// src/fraud_graph/static/js/sheet_crafter.js

function openTinDataDialog(sexFieldName, dobFieldName, tinFieldName) {
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
});