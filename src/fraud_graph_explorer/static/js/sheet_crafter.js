// src/fraud_graph/static/js/sheet_crafter.js

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

function openTinDataDialog(sexFieldName, dobFieldName, tinFieldName) {
    // Check the TIN's country override select
    // Only fire the modal for algorithmic TINs (IT/FR).
    // For DE/ES/GB, the TIN is a random pool value — no modal needed.
    const tinCountrySelect = document.getElementById('id_' + tinFieldName + '_country');
    const tinCountry = tinCountrySelect ? tinCountrySelect.value : null;

    if (tinCountry !== 'IT' && tinCountry !== 'FR') {
        // DE/ES/GB: TIN is independent of the name — no modal, no recalc
        return;
    }
    // ────────────────────────────────────────────────────────

    const dialog = document.getElementById('tin-data-dialog');

    // Store the target field IDs on the dialog element
    dialog.dataset.sexTarget = 'id_' + sexFieldName;
    dialog.dataset.dobTarget = 'id_' + dobFieldName;
    dialog.dataset.tinTarget = 'id_' + tinFieldName;

    // Pre-fill the modal inputs with the current hidden field values
    const currentSexInput = document.getElementById(dialog.dataset.sexTarget);
    const currentDobInput = document.getElementById(dialog.dataset.dobTarget);

    document.getElementById('modal-sex-select').value = currentSexInput.value || "";
    document.getElementById('modal-dob-input').value = currentDobInput.value || "";
    document.getElementById('modal-recalc-tin').checked = true; // Reset to checked

    // Set the recalc label based on the TIN's override country
    const recalcLabel = document.getElementById('modal-recalc-tin-label');
    if (recalcLabel) {
        const labels = window.MODAL_RECALC_LABELS || {};
        recalcLabel.textContent = labels[tinCountry] || '';
    }

    dialog.showModal();
}

// Listen for the form submission inside the dialog
document.getElementById('tin-data-form').addEventListener('submit', e => {
    e.preventDefault(); // Stop auto-closing so we can trigger HTMX first

    const selectedSex = document.getElementById('modal-sex-select').value;
    const selectedDob = document.getElementById('modal-dob-input').value;

    // Native required validation check
    if (!selectedSex || !selectedDob) {
        return;
    }

    const dialog = document.getElementById('tin-data-dialog');
    const sexTarget = document.getElementById(dialog.dataset.sexTarget);
    const dobTarget = document.getElementById(dialog.dataset.dobTarget);
    const tinTarget = document.getElementById(dialog.dataset.tinTarget);

    // Update the hidden inputs in the main form
    if (sexTarget) sexTarget.value = selectedSex;
    if (dobTarget) dobTarget.value = selectedDob;

    // Check if we should auto-recalculate the TIN
    const recalcChecked = document.getElementById('modal-recalc-tin').checked;

    // Close the modal
    dialog.close();

    if (recalcChecked && tinTarget) {
        // Find the recalculate span associated with this TIN input
        const recalcBtn = tinTarget.parentElement.querySelector('.recalc-icon');
        if (recalcBtn) {
            // Programmatically click the button! HTMX will handle the rest.
            recalcBtn.click();
        }
    }
});


// Fix for Firefox restoring form state on refresh
document.addEventListener('DOMContentLoaded', () => {
    // Find all text and date inputs inside the form container
    const inputs = document.querySelectorAll('#form-container input[type="text"], #form-container input[type="date"]');
    inputs.forEach(input => {
        // Force the visual value to match the HTML value attribute Django rendered
        if (input.defaultValue !== undefined) {
            input.value = input.defaultValue;
        }
    });

    // Fix selects (Firefox restores select values on refresh)
    // Reset each select to the option that has the "selected" attribute
    // in the server-rendered HTML (i.e., the default value Django set).
    const selects = document.querySelectorAll('#form-container select');
    selects.forEach(select => {
        const defaultOption = select.querySelector('option[selected]');
        if (defaultOption) {
            select.value = defaultOption.value;
        }
    });
});

/**
 * Update an input's value from an HTMX response.
 * Used by the country override selects — the endpoint returns
 * the new value as plain text, and this function sets it on the input.
 *
 * HTMX's default swap (innerHTML) doesn't work on <input> elements
 * (void elements have no inner HTML), so we use hx-swap="none" + this
 * callback instead.
 */
function updateFieldValue(inputId, event) {
    if (event.detail.xhr.status !== 200) return;

    const data = JSON.parse(event.detail.xhr.responseText.trim());
    const input = document.getElementById(inputId);

    if (input && data.value !== undefined) {
        input.value = data.value;
    }

    // Populate hidden calc fields (sex, dob, birthplace)
    if (data.updates) {
        for (const [fieldName, fieldValue] of Object.entries(data.updates)) {
            const fieldInput = document.getElementById('id_' + fieldName);
            if (fieldInput) {
                fieldInput.value = fieldValue;
            }
        }
    }

    // Update the tooltip text based on the selected country
    const select = event.detail.requestConfig.elt;
    if (select && window.FIELD_HINTS) {
        const country = select.value;
        const container = select.closest('.input-group-vat, .input-group-tin, .input-group-iban');
        if (container) {
            const tooltipEl = container.querySelector('[data-bs-toggle="tooltip"][data-hint-key]');
            if (tooltipEl) {
                const hintKey = tooltipEl.dataset.hintKey;
                const hints = window.FIELD_HINTS[hintKey];
                if (hints && typeof hints === 'object' && hints[country]) {
                    console.log(hints[country]);
                    // Update the tooltip content
                    tooltipEl.setAttribute('data-bs-title', hints[country]);
                    const tooltip = bootstrap.Tooltip.getInstance(tooltipEl);
                    if (tooltip) {
                        tooltip.setContent({ '.tooltip-inner': hints[country] });
                    }
                }
            }
        }
    }
}


// ─── Bootstrap tooltip initialization ───
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

// Re-initialize after HTMX swaps (when form is re-rendered on country change)
document.body.addEventListener('htmx:afterSettle', initTooltips);


// ─── Auto-highlight fields that exceed maxlength ───
// The browser's :invalid pseudo-class doesn't trigger on pre-filled
// values until the user interacts. This manually checks on load + on
// every edit, so invalid fields are highlighted immediately and the
// highlight auto-removes when the user fixes the value.
function checkFieldValidity(input) {
    var maxLen = parseInt(input.getAttribute('maxlength'), 10);

    if (maxLen && input.value.length > maxLen) {
        // ─── Invalid: add red border + tooltip with error message ───
        input.classList.add('is-invalid');

        var msg = 'Maxi ' + maxLen + ' characters<br>(currently ' + input.value.length + ')';

        // Set tooltip attributes (so initTooltips can also manage it)
        input.setAttribute('data-bs-toggle', 'tooltip');
        input.setAttribute('data-bs-title', msg);
        input.setAttribute('data-bs-custom-class', 'crafter-tooltip');

        // Create or update the Bootstrap tooltip
        var tooltip = bootstrap.Tooltip.getOrCreateInstance(input, {
            container: 'body',
            placement: 'top',
            html: true,
            sanitize: false
        });
        tooltip.setContent({ '.tooltip-inner': msg });

    } else {
        // ─── Valid: remove red border + dispose tooltip ───
        input.classList.remove('is-invalid');

        // Dispose the tooltip instance (hides + removes from DOM)
        var tooltip = bootstrap.Tooltip.getInstance(input);
        if (tooltip) {
            tooltip.dispose();
        }

        // Remove tooltip attributes
        input.removeAttribute('data-bs-toggle');
        input.removeAttribute('data-bs-title');
        input.removeAttribute('data-bs-custom-class');
    }
}

function initMaxlengthValidation() {
    document.querySelectorAll('input[maxlength], textarea[maxlength]').forEach(function(input) {
        // Check immediately (catches pre-filled values from server)
        checkFieldValidity(input);

        // Re-check on every edit (auto-remove highlight when fixed)
        input.addEventListener('input', function() {
            checkFieldValidity(input);
        });
    });
}

// Run on page load
document.addEventListener('DOMContentLoaded', initMaxlengthValidation);

// Re-run after HTMX swaps (if the form is re-rendered)
document.body.addEventListener('htmx:afterSettle', initMaxlengthValidation);


document.addEventListener('DOMContentLoaded', function() {
    var firstInvalid = document.querySelector('.is-invalid');
    if (firstInvalid) {
        firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstInvalid.focus();
    }
});