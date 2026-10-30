// src/fraud_graph/static/js/sheet_crafter.js

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
    if (event.detail.xhr.status === 200) {
        const input = document.getElementById(inputId);
        if (input) {
            input.value = event.detail.xhr.responseText.trim();
        }
    }

    // Update the tooltip text based on the selected country
    const select = event.detail.requestConfig.elt;
    if (select && window.FIELD_HINTS) {
        const country = select.value;
        const container = select.closest('.input-group, .input-group-tin');
        if (container) {
            const tooltipText = container.querySelector('.tooltip-text[data-hint-key]');
            if (tooltipText) {
                const hintKey = tooltipText.dataset.hintKey;
                const hints = window.FIELD_HINTS[hintKey];
                if (hints && typeof hints === 'object' && hints[country]) {
                    tooltipText.innerHTML = hints[country];
                }
            }
        }
    }
}