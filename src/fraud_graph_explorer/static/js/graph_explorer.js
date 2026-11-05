// src/fraud_graph_explorer/static/js/graph_explorer.js

/*
# Fraud Graph Explorer
# Copyright (C) 2026 Luca Amodeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

let network = null; // Global Vis.js network instance

let deleteSheetId = null;
// Open the Delete Modal
function openDeleteDialog(sheetId, reqNum) {
    deleteSheetId = sheetId;

    const reqNumSpan = document.getElementById('del-req-num');
    if (reqNumSpan) {
        reqNumSpan.innerText = reqNum;
    }

    // Use Bootstrap JS to show the modal
    const modalEl = document.getElementById('deleteModal');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
}
// Confirm Delete (Send HTMX request and hide modal)
function confirmDelete() {
    if (!deleteSheetId) return;

    const deleteUrl = `/explorer/delete/${deleteSheetId}/`;

    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const headers = {};
    if (csrfInput) {
        headers['X-CSRFToken'] = csrfInput.value;
    }

    // Send the delete request.
    // Django will return empty HTML and the 'deleteSuccess' trigger.
    htmx.ajax('POST', deleteUrl, {
        target: '#ingest-status',
        swap: 'innerHTML',
        headers: headers
    });

    // Use Bootstrap JS to hide the modal
    const modalEl = document.getElementById('deleteModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();

    deleteSheetId = null;
}
// Listen for the delete success event
document.body.addEventListener('deleteSuccess', function(evt) {
    // Django sends both the new list URL and the deleted sheet_id
    const targetUrl = evt.detail.value;
    const deletedSheetId = evt.detail.sheet_id;

    // Update the browser URL so F5/Refresh works perfectly
    history.pushState({}, '', targetUrl);

    // Sync the Firefox dropdowns and inputs!
    const urlParams = new URLSearchParams(targetUrl.split('?')[1] || '');
    const form = document.getElementById('filter-form');
    if (form) {
        form.querySelectorAll('input, select').forEach(input => {
            if (input.name) {
                input.value = urlParams.get(input.name) || '';
            }
        });
    }

    // Fetch the updated list (Page 1 with filters)
    htmx.ajax('GET', targetUrl, {
        target: '#applications-list',
        swap: 'innerHTML'
    });

    // Reset graph + detail panes if the deleted sheet was being shown
    if (deletedSheetId) {
        if (window.currentRootSheet === deletedSheetId) {
            // Deleted sheet was the ROOT → reset everything (root + linked + graph + cards)
            resetRootSheetView();
        } else if (window.currentLinkedSheet === deletedSheetId) {
            // Deleted sheet was only the LINKED side → clear just that pane
            resetLinkedPane();
        }
    }
});

/**
 * Return the pre-rendered empty-state HTML for the detail panes.
 * The markup + translated message live in <template id="empty-state">
 * inside dashboard.html, which itself delegates to _empty_state.html
 * so the initial render and all JS-driven resets share one source of truth.
 */
function getEmptyStateHtml() {
    const tpl = document.getElementById('empty-state');
    if (!tpl) {
        // Defensive fallback — should never happen
        return '<p class="text-muted fst-italic">—</p>';
    }
    return tpl.innerHTML;
}


function resetRootSheetView() {
    // Clear the Vis.js graph
    if (network) {
        network.body.data.nodes.clear();
        network.body.data.edges.clear();
        network.redraw();
    }
    window.currentRootSheet = null;
    window.currentLinkedSheet = null;

    const emptyHtml = getEmptyStateHtml();
    const rootPane   = document.getElementById('root-detail-pane');
    const linkedPane = document.getElementById('linked-detail-pane');
    if (rootPane)   rootPane.innerHTML   = emptyHtml;
    if (linkedPane) linkedPane.innerHTML = emptyHtml;

    // Clear the cards panel (errors/warnings)
    const cardsPanel = document.getElementById('ingest-status');
    if (cardsPanel) cardsPanel.innerHTML = '';

    // ─── NEW: clear any evidence highlights (no shared values to highlight anymore) ───
    updateEvidenceHighlights();

    // If user is on Tab 2 or Tab 3, jump back to Tab 1
    const activeTab = document.querySelector('.nav-link.active');
    if (activeTab && (activeTab.dataset.tab === 'tab2' || activeTab.dataset.tab === 'tab3')) {
        openTab('tab1');
    }
}


function resetLinkedPane() {
    const emptyHtml = getEmptyStateHtml();
    const linkedPane = document.getElementById('linked-detail-pane');
    if (linkedPane) linkedPane.innerHTML = emptyHtml;

    window.currentLinkedSheet = null;

    // ─── NEW: clear evidence highlights (linked sheet is gone) ───
    // The root pane still has content, but with no linked sheet, there are
    // no shared values to highlight — clear any stale highlights from the
    // previous linked sheet.
    updateEvidenceHighlights();
}

/**
 * Highlight (or clear) occurrences of `evidenceWords` in the given DOM elements.
 * Wraps matches in <mark class="evidence-highlight">.
 *
 * To clear: call with an empty evidenceWords array.
 *
 * Each pane gets its own highlight color via CSS:
 *   #root-detail-pane .evidence-highlight   → purple bg (matching old PoC root color)
 *   #linked-detail-pane .evidence-highlight → red bg   (matching old PoC selected color)
 *
 * (CSS classes already defined in your style.css.)
 */
function applyEvidence(elements, evidenceWords) {
    if (!elements || elements.length === 0) {
        console.warn("applyEvidence: No elements provided.");
        return;
    }

    // ─── Cleanup previous highlights ───
    elements.forEach(element => {
        const highlights = element.querySelectorAll('.evidence-highlight');
        highlights.forEach(highlight => {

            // ─── CHANGED: dispose Bootstrap tooltip before removing the span ───
            // Otherwise the tooltip div (appended to <body>) becomes an orphan
            // and accumulates on every re-selection.
            const tip = bootstrap.Tooltip.getInstance(highlight);
            if (tip) tip.dispose();
            // ────────────────────────────────────────────────────────────────────

            const parent = highlight.parentNode;
            parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
            parent.normalize();
        });
        delete element.dataset.evidenceApplied;
    });

    // ─── Early exit if no new evidence words ───
    if (!evidenceWords || evidenceWords.length === 0) {
        return;
    }

    // ─── Build regex (longer phrases first to prevent partial matches) ───
    const validWords = evidenceWords.filter(w => w && w.trim() !== '');
    if (validWords.length === 0) return;

    validWords.sort((a, b) => b.length - a.length);

    // Escape regex special chars
    const escapedWords = validWords.map(word =>
        word.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')
    );

    // Word boundaries: (?<!\w) and (?!\w) — works for both words and phrases
    const regexParts = escapedWords.map(word => `(?<!\\w)${word}(?!\\w)`);
    const regex = new RegExp(regexParts.join('|'), 'gi');

    // ─── Apply new highlights ───
    elements.forEach(element => {
        const originalHTML = element.innerHTML;
        // ─── CHANGED: title= → data-bs-toggle + data-bs-title + custom class ───
        const modifiedHTML = originalHTML.replace(regex, match =>
            `<span class="evidence-highlight" ` +
                `data-bs-toggle="tooltip" ` +
                `data-bs-title="${window.EVIDENCE_LINKED_TOOLTIP || ''}" ` +
                `data-bs-custom-class="explorer-tooltip">` +
                `<i class="bi bi-arrow-left-right evidence-icon me-2"></i>` +
                `<span class="evidence-text">${match}</span>` +
            `</span>`
        );

        if (modifiedHTML !== originalHTML) {
            element.innerHTML = modifiedHTML;
            element.dataset.evidenceApplied = 'true';

            // ─── CHANGED: initialize Bootstrap tooltips on the new spans ───
            // innerHTML insertion doesn't trigger initTooltips() (these spans
            // aren't present at HTMX swap time — they're created dynamically
            // by this function after the swap settles).
            element.querySelectorAll('.evidence-highlight').forEach(span => {
                bootstrap.Tooltip.getOrCreateInstance(span, {
                    container: 'body',
                    html: true,
                    sanitize: false
                });
            });
        }
    });
}

/**
 * Extract the entity values shared between the root sheet and the linked sheet.
 * These are the values that should be highlighted in BOTH detail panes —
 * they represent the forensic "link" between the two sheets.
 *
 * Reads from network.body.data (the in-memory Vis.js dataset) — no API call.
 *
 * Returns: array of strings (full entity values, not truncated labels).
 *          Empty if either sheet is not loaded, or no shared entities exist.
 */
function getSharedEntityValues() {
    if (!network) return [];
    if (!window.currentRootSheet || !window.currentLinkedSheet) return [];

    const rootId = `sheet_${window.currentRootSheet}`;
    const linkedId = `sheet_${window.currentLinkedSheet}`;
    const edges = network.body.data.edges.get();
    const nodes = network.body.data.nodes;

    // ─── Get entity IDs connected to root ───
    const rootConnected = new Set();
    edges.forEach(edge => {
        if (edge.from === rootId && edge.to.startsWith('ent_')) {
            rootConnected.add(edge.to);
        } else if (edge.to === rootId && edge.from.startsWith('ent_')) {
            rootConnected.add(edge.from);
        }
    });

    // ─── Get entity IDs connected to linked ───
    const linkedConnected = new Set();
    edges.forEach(edge => {
        if (edge.from === linkedId && edge.to.startsWith('ent_')) {
            linkedConnected.add(edge.to);
        } else if (edge.to === linkedId && edge.from.startsWith('ent_')) {
            linkedConnected.add(edge.from);
        }
    });

    // ─── Intersection: entities connected to BOTH ───
    const sharedIds = [...rootConnected].filter(id => linkedConnected.has(id));

    // ─── Build evidence words list ───
    // Include BOTH:
    //   - The normalized value (node.title or node.label) — for cases where
    //     the detail pane happens to show the normalized form (rare)
    //   - All raw values (node.raw_values) — for the common case where the
    //     detail pane shows the original PDF text with spaces/dashes/case
    //
    // Dedupe via a Set so the same string isn't passed twice.
    const evidenceWords = [];
    const seen = new Set();

    sharedIds.forEach(entId => {
        const node = nodes.get(entId);
        if (!node) return;

        // Normalized value (full, from title or label)
        const normalizedValue = node.title || node.label;
        if (normalizedValue && !seen.has(normalizedValue)) {
            evidenceWords.push(normalizedValue);
            seen.add(normalizedValue);
        }

        // All raw values (root's + each linked sheet's)
        if (node.raw_values && Array.isArray(node.raw_values)) {
            node.raw_values.forEach(rv => {
                if (rv && !seen.has(rv)) {
                    evidenceWords.push(rv);
                    seen.add(rv);
                }
            });
        }
    });

    return evidenceWords;
}


/**
 * Update highlights in BOTH detail panes based on the current root + linked sheets.
 *
 * - If both root + linked are loaded → highlights shared entity values
 * - If only root is loaded (no linked yet) → clears previous highlights
 * - If neither is loaded → clears all highlights
 *
 * Called after every HTMX swap on either pane, and on reset functions.
 *
 * Idempotent: safe to call multiple times. Each call clears previous highlights
 * before applying new ones.
 */
function updateEvidenceHighlights() {
    const rootPane = document.getElementById('root-detail-pane');
    const linkedPane = document.getElementById('linked-detail-pane');

    if (!rootPane || !linkedPane) return;

    const rootTable = rootPane.querySelector('.sheet-detail-table');
    const linkedTable = linkedPane.querySelector('.sheet-detail-table');

    if (!rootTable || !linkedTable) {
        // One of the tables isn't rendered yet (e.g., empty state) — nothing to do
        return;
    }

    const sharedValues = getSharedEntityValues();
    applyEvidence([rootTable, linkedTable], sharedValues);
}

// Function to highlight row and load cards
function selectAppForCards(row) {
    // Remove highlight from other rows
    document.querySelectorAll('#applications-list tr.selected').forEach(el => el.classList.remove('selected'));
    // Highlight clicked row
    row.classList.add('selected');
}


// Remove Filter Logic
// Remove a specific filter by its name attribute
function removeFilter(filterName) {
    // Find the form element
    let input = document.querySelector(`#filter-form [name="${filterName}"]`);
    if (input) {
        input.value = ''; // Clear the value
        // Trigger HTMX to reload the list
        htmx.trigger('#filter-form', 'submit');
    }
}
// Clear all filters at once
function clearFilters() {
    let inputs = document.querySelectorAll('#filter-form input, #filter-form select');
    inputs.forEach(input => input.value = '');
    htmx.trigger('#filter-form', 'submit');
}


// Auto-select the newly uploaded PDF
let pendingSelectSheetId = null;
// Catch the event, but DON'T try to find the row yet!
document.body.addEventListener('selectNewApp', function(evt) {
    // HTMX sometimes wraps strings in an object, so we handle both
    pendingSelectSheetId = evt.detail.value || evt.detail;
    console.log("==> selectNewApp fired! Waiting for list to reload...", pendingSelectSheetId);
    clearFilters();
});

// Listen for HTMX to finish loading the applications list
const appList = document.getElementById('applications-list');
if (appList) {
    appList.addEventListener('htmx:afterSettle', function() {
        // If we have a pending sheet to select, NOW we try to find it
        if (pendingSelectSheetId) {
            console.log("==> List settled! Looking for row:", pendingSelectSheetId);
            let newRow = document.getElementById('row-' + pendingSelectSheetId);

            if (newRow) {
                console.log("==> newRow OK");
                selectAppForCards(newRow);

                // Use swap: 'none' so it ONLY processes the OOB swaps!
                // This prevents the success badge from being overwritten.
                htmx.ajax('GET', `/explorer/cards/${pendingSelectSheetId}/`, {
                    // the target isn't touched at all: it is only a placeholder here...
                    target: '#ingest-status',
                    swap: 'none'
                });

                // Preload graph + detail panel for the new sheet
                preloadApplication(pendingSelectSheetId);
            }
            // Clear the pending ID so it doesn't trigger again on normal pagination
            pendingSelectSheetId = null;
        }
    });
}


// Toggle Physics Engine on/off
function togglePhysics(isChecked) {
    if (!network) return;

    // Turn the physics simulation on or off
    network.setOptions({ physics: isChecked });

    // If turning it back on, re-stabilize the graph so it settles nicely
    if (isChecked) {
        network.stabilize();
    }
}


// Force all checkboxes to checked on every graph load
function resetLegendCheckboxes() {
    document.querySelectorAll('#graph-legend input[type="checkbox"]').forEach(cb => {
        cb.checked = true;
    });
}


// Function to hide/show node groups from the Legend checkboxes
function toggleGroup(groupName, isChecked) {
    if (!network) return;

    const nodesDataset = network.body.data.nodes;
    const entityUpdates = [];
    const linkedSheetUpdates = [];

    // Step 1: Hide/Show the entities of the toggled group
    nodesDataset.get().forEach(node => {
        if (node.group === groupName) {
            entityUpdates.push({ id: node.id, hidden: !isChecked });
        }
    });
    nodesDataset.update(entityUpdates);

    // Step 2: Re-evaluate all Linked Sheets (Cascading effect)
    const allNodes = nodesDataset.get();

    allNodes.forEach(node => {
        if (node.group === 'Linked_Sheet') {
            // Get all entities connected to this linked sheet
            const connectedNodes = network.getConnectedNodes(node.id);

            // Check if at least one connected entity is VISIBLE
            const hasVisibleConnection = connectedNodes.some(connId => {
                const connNode = nodesDataset.get(connId);
                // If the connected node is an entity (not the Root Sheet) and is not hidden
                return connNode && connNode.group !== 'Root_Sheet' && !connNode.hidden;
            });

            // If no visible connections, hide the linked sheet. Otherwise, show it.
            linkedSheetUpdates.push({ id: node.id, hidden: !hasVisibleConnection });
        }
    });

    if (linkedSheetUpdates.length > 0) {
        nodesDataset.update(linkedSheetUpdates);
    }
}

function openTab(tabId) {
    let tabs = document.querySelectorAll('.dashboard-tab');

    // 1. Hide all tabs, remove ALL display/flex classes
    tabs.forEach(t => {
        t.classList.add('d-none');
        t.classList.remove('d-flex', 'd-block', 'flex-row', 'flex-column', 'active');
    });

    // Show selected tab and set active state
    let tab = document.getElementById(tabId);
    tab.classList.remove('d-none');
    tab.classList.add('active'); // <-- Add active to the new tab

    // Add the correct display and flex-direction classes (d-flex for 1,2,3 and d-block for 4)
    if (tabId === 'tab4') {
        tab.classList.add('d-block');
    } else if (tabId === 'tab1') {
        tab.classList.add('d-flex', 'flex-column');
    } else { // tab2 and tab3
        tab.classList.add('d-flex', 'flex-row');
    }

    // Update active button state in the nav
    let links = document.querySelectorAll('.nav-link');
    links.forEach(l => l.classList.remove('active'));

    let activeBtn = document.querySelector(`.nav-link[data-tab="${tabId}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    // Trigger Vis.js redraw if opening Graph Tab
    if (tabId === 'tab2' && network !== null) {
        setTimeout(() => {
            network.redraw();   // recompute canvas dimensions
            network.fit();      // recenter camera on all nodes
        }, 100);
    }
}

// Inner: fetch only — no highlight, no tab switch
function preloadApplication(sheetId) {
    // Load Root Details into Tab 3 pane (will be visible when user opens Tab 3)
    htmx.ajax('GET', `/explorer/detail/${sheetId}/`, {
        target: '#root-detail-pane',
        swap: 'innerHTML'
    });

    // Track the new root sheet + clear stale linked-sheet reference
    window.currentRootSheet = sheetId;
    window.currentLinkedSheet = null;   // previous linked sheet is no longer valid

    // ─── NEW: clear the linked pane — switching root invalidates the previous linked sheet ───
    const linkedPane = document.getElementById('linked-detail-pane');
    if (linkedPane) linkedPane.innerHTML = getEmptyStateHtml();

    // ─── NEW: clear any stale highlights (no linked sheet → no shared values to highlight) ───
    updateEvidenceHighlights();

    // Prepare Graph Data for Tab 2 (will be re-fit when user opens Tab 2)
    loadGraphData(sheetId);
}
// Outer: highlight row + switch tab + preload
function loadApplication(sheetId, targetTab, btn) {
    // Highlight the selected row
    document.querySelectorAll('tr.selected').forEach(el => el.classList.remove('selected'));
    if (btn) {
        btn.closest('tr').classList.add('selected');
    }

    // Switch to the requested tab (Graph or Details)
    openTab(targetTab);

    // Preload graph + detail
    preloadApplication(sheetId);
}


// Function to load the right pane (Linked Sheet) when a Vis.js node is clicked
function loadLinkedDetail(sheetId) {
    window.currentLinkedSheet = sheetId;   // track for delete-sync
    const detailUrl = `/explorer/detail/${sheetId}/`;
    htmx.ajax('GET', detailUrl, { target: '#linked-detail-pane', swap: 'innerHTML' });
}

const rootStyle = getComputedStyle(document.documentElement);
const rootBrdColor = rootStyle.getPropertyValue('--root-brd-color').trim();
const rootBgColor = rootStyle.getPropertyValue('--root-bg-color').trim();
const linkedBrdColor = rootStyle.getPropertyValue('--linked-brd-color').trim();
const linkedBgColor = rootStyle.getPropertyValue('--linked-bg-color').trim();

// Define i2-style Colors & Shapes based on "group"
const options = {
    groups: {
        'Root_Sheet': {
            chosen: {
                label: false,
            },
            color: {
                border: rootBrdColor,
                background: rootBgColor,
                hover: { border: rootBrdColor, background: rootBgColor },
                highlight: { border: rootBrdColor, background: rootBgColor }
            },
            font: {
                multi: 'html',
                color: '#ffffff',
                size: 14,
                face: '"Noto Flags", Helvetica, Arial, sans-serif',
                vadjust: 0,
                bold: {
                    color: '#ffff00',
                    vadjust: 0,
                    mod: 'bold'
                },
                ital: {
                    color: '#ffffff',
                    vadjust: 0,
                    mod: 'italic'
                },
                boldital: {
                    color: '#ffffff',
                    size: 24,
                    face: '"Noto Flags", Helvetica, Arial, sans-serif',
                    vadjust: 0,
                    mod: 'bold italic'
                },
                mono: {
                    size: 16,
                    color: '#ffff00',
                    vadjust: 0,
                    mod: ''
                }
            },
            shape: 'box',
            borderWidth: 2,
            margin: 12,
            widthConstraint: { minimum: 100, maximum: 300 }
         },
        'Linked_Sheet': {
            chosen: {
                label: false,
            },
            color: {
                border: linkedBrdColor,
                background: linkedBgColor,
                hover: { border: linkedBrdColor, background: linkedBgColor },
                highlight: { border: linkedBgColor, background: linkedBrdColor }
            },
            font: {
                multi: 'html',
                color: '#ffffff',
                size: 14,
                face: '"Noto Flags", Helvetica, Arial, sans-serif',
                vadjust: 0,
                bold: {
                    color: '#ffff00',
                    vadjust: 0,
                    mod: 'bold'
                },
                ital: {
                    color: '#ffffff',
                    vadjust: 0,
                    mod: 'italic'
                },
                boldital: {
                    color: '#ffffff',
                    size: 24,
                    face: '"Noto Flags", Helvetica, Arial, sans-serif',
                    vadjust: 0,
                    mod: 'bold italic'
                },
                mono: {
                    size: 16,
                    color: '#ffff00',
                    vadjust: 0,
                    mod: ''
                }
            },
            shape: 'box',
            borderWidth: 2,
            margin: 12,
            widthConstraint: { minimum: 100, maximum: 300 }
        },

        // SPREAD THE DYNAMIC GROUPS HERE!
        ...window.ENTITY_GRAPH_GROUPS

    },
    nodes: {
        shape: 'box',
        font: { size: 12, color: '#ffffff', multi: 'html' },
        borderWidth: 1,
    },
    edges: {
        smooth: { type: 'continuous' },
        font: { size: 12, color: '#333', strokeWidth: 3, strokeColor: '#ffffff', align: 'top' }
    },
    physics: {
        forceAtlas2Based: {
            gravitationalConstant: -50,
            centralGravity: 0.01,
            springLength: 100,
            avoidOverlap: 1
        },
        solver: 'forceAtlas2Based',
        enabled: true,
        stabilization: {
            enabled: true,
            iterations: 150,
            updateInterval: 25
        }
    },
    interaction: {
        hover: true,
        zoomView: true,
        zoomSpeed: 0.5,
        dragView: true,
        dragNodes: true,
        navigationButtons: true,
        keyboard: true
    }
};


async function loadGraphData(sheetId) {
    const container = document.getElementById('vis-canvas');
    if (!container) return;

    // CALL RESET CHECKBOXES HERE
    resetLegendCheckboxes();

    // Get reference to the physics switch
    const physicsToggle = document.getElementById('toggle-physics');

    // Fetch graph data from Django API
    try {
        const response = await fetch(`/explorer/api/graph/${sheetId}/`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();

        // PRELOAD ALL ENTITY IMAGES TO FIX VIS.JS Z-INDEX BUG
        if (window.ENTITY_GRAPH_GROUPS) {
            const preloadPromises = Object.values(window.ENTITY_GRAPH_GROUPS).map(g => {
                if (g.shape === 'circularImage' && g.image) {
                    return new Promise((resolve) => {
                        const img = new Image();
                        img.src = g.image;
                        img.onload = () => resolve();
                        img.onerror = () => resolve(); // Resolve even on error to not block graph
                    });
                }
                return Promise.resolve();
            });
            // Wait for all 9 images to be loaded in the browser cache
            await Promise.all(preloadPromises);
        }

        // Manage Physics Toggle state
        if (data.nodes.length > 0) {
            physicsToggle.disabled = false;
            physicsToggle.checked = true;   // Explicitly set to ON when loading new data
        } else {
            physicsToggle.disabled = true;  // Disable if empty
            physicsToggle.checked = false;
        }


        // Initialize or update Vis.js Network
        const nodesDataset = new vis.DataSet(data.nodes);
        const edgesDataset = new vis.DataSet(data.edges);

        // Define what happens when stabilization finishes
        function onStabilized() {
            network.setOptions({ physics: false });
            network.fit({ animation: { duration: 500, easingFunction: "easeInOutQuad" } });
            physicsToggle.checked = false;
        }


        if (network === null) {
            network = new vis.Network(container, { nodes: nodesDataset, edges: edgesDataset }, options);

            network.once("stabilizationIterationsDone", onStabilized);

            // Event Listeners for Analyst Interaction (Only bound once)
            // Populate/Clear details when a node is selected
            network.on("selectNode", function(params) {
                if (params.nodes.length === 0) return;

                const nodeId = params.nodes[0];

                // Only Linked Sheet nodes change the linked pane.
                // Root Sheet clicks: do nothing (pane stays showing the current linked sheet)
                // Entity clicks:     do nothing (pane stays showing the current linked sheet)
                // Edge clicks:       don't fire selectNode at all (Vis.js doesn't select edges via click by default)
                if (!nodeId.startsWith('sheet_')) {
                    return;   // entity node — ignore
                }

                const selectedSheetId = nodeId.replace('sheet_', '');

                // Skip the Root Sheet — don't clear the linked pane
                if (selectedSheetId === window.currentRootSheet) {
                    return;
                }

                // It's a Linked Sheet — load its details (replaces previous)
                loadLinkedDetail(selectedSheetId);
            });

            // Populate/Clear details when a node drag ends
            network.on("dragEnd", function(params) {
                if (params.nodes.length === 0) return;

                const nodeId = params.nodes[0];

                if (!nodeId.startsWith('sheet_')) {
                    return;   // dragged an entity — ignore
                }

                const draggedSheetId = nodeId.replace('sheet_', '');

                // Skip the Root Sheet
                if (draggedSheetId === window.currentRootSheet) {
                    return;
                }

                // It's a Linked Sheet — load its details
                loadLinkedDetail(draggedSheetId);
            });

//            // Empty details when a node is deselected (e.g., clicking empty canvas)
//            network.on("deselectNode", function(params) {
//                const pane = document.getElementById('linked-detail-pane');
//                if (pane) pane.innerHTML = getEmptyStateHtml();
//            });

            // Double-click to make new root (Excluding the Root Sheet itself)
            network.on("doubleClick", function(params) {
                if (params.nodes.length > 0) {
                    const nodeId = params.nodes[0];
                    if (nodeId.startsWith('sheet_')) {
                        // Double click a Sheet -> Make it the new Root!
                        const newRootSheetId = nodeId.replace('sheet_', '');
                        // FIX: Exclude the Root Sheet!
                        // If they double-click the root, do nothing (don't reload the same graph)
                        if (newRootSheetId !== window.currentRootSheet) {
                            window.currentRootSheet = newRootSheetId;
                            loadApplication(newRootSheetId, 'tab2', null);
                            // Reload the graph with the new root
                            loadGraphData(newRootSheetId);
                        }
                    }
                }
            });

        } else {
            // Update data and explicitly re-enable physics for the new nodes
            //network.setOptions(options);
            network.setOptions({ physics: true });
            network.setData({ nodes: nodesDataset, edges: edgesDataset });

            // 2. EXPLICITLY FORCE STABILIZATION!
            // This guarantees 'stabilizationIterationsDone' fires, even for tiny graphs.
            network.stabilize();
            network.once("stabilizationIterationsDone", onStabilized);
        }

        // Store globally for redraws
        window.currentNetwork = network;

    } catch (error) {
        console.error('Error fetching graph data:', error);
        container.innerHTML = '<p style="color:red; text-align:center; margin-top:50px;">Failed to load graph data.</p>';
        physicsToggle.disabled = true;
        physicsToggle.checked = false;
    }
}



// ─── Wire up HTMX afterSettle listeners for evidence highlighting ───
// Whenever either detail pane gets new content (via HTMX swap), recompute
// the shared entity values and re-apply highlights.
//
// Order of operations when user clicks a Linked Sheet node:
//   1. selectNode fires → calls loadLinkedDetail(newLinkedId)
//   2. loadLinkedDetail sets window.currentLinkedSheet = newLinkedId
//   3. loadLinkedDetail triggers htmx.ajax → fetches + swaps linked pane
//   4. htmx:afterSettle fires on #linked-detail-pane (this listener)
//   5. updateEvidenceHighlights() runs:
//        - reads currentRootSheet + currentLinkedSheet (both set)
//        - getSharedEntityValues() finds entity nodes connecting both
//        - applyEvidence([rootPane, linkedPane], sharedValues) highlights them

const _rootPaneForEvidence = document.getElementById('root-detail-pane');
const _linkedPaneForEvidence = document.getElementById('linked-detail-pane');

if (_rootPaneForEvidence) {
    _rootPaneForEvidence.addEventListener('htmx:afterSettle', updateEvidenceHighlights);
}
if (_linkedPaneForEvidence) {
    _linkedPaneForEvidence.addEventListener('htmx:afterSettle', updateEvidenceHighlights);
}


// --- Bootstrap tooltip initialization ---
function initTooltips() {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        bootstrap.Tooltip.getOrCreateInstance(el, {
            container: 'body',
            html: true,
            sanitize: false
        });
    });
    // Force Chrome to flush its hit-test cache
    document.body.getBoundingClientRect();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initTooltips);

// Re-initialize after HTMX swaps (detail panes, filter results, badges)
document.body.addEventListener('htmx:afterSettle', initTooltips);