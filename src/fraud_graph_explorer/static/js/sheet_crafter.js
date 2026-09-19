// src/fraud_graph/static/js/sheet_crafter.js

function openTinDataDialog(sexFieldName, dobFieldName) {
    const dialog = document.getElementById('tin-data-dialog');

    // Store the target field IDs on the dialog element
    dialog.dataset.sexTarget = 'id_' + sexFieldName;
    dialog.dataset.dobTarget = 'id_' + dobFieldName;

    // Pre-fill the modal inputs with the current hidden field values
    const currentSexInput = document.getElementById(dialog.dataset.sexTarget);
    const currentDobInput = document.getElementById(dialog.dataset.dobTarget);

    document.getElementById('modal-sex-select').value = currentSexInput.value || "";
    document.getElementById('modal-dob-input').value = currentDobInput.value || "";

    dialog.showModal();
}

// Listen for the form submission inside the dialog
document.getElementById('tin-data-form').addEventListener('submit', e => {
    // We do NOT use e.preventDefault() here!
    // This allows the browser's native 'required' validation to work.
    // If validation passes, the browser natively closes the dialog (because method="dialog").

    const dialog = document.getElementById('tin-data-dialog');
    const sexTarget = document.getElementById(dialog.dataset.sexTarget);
    const dobTarget = document.getElementById(dialog.dataset.dobTarget);

    // Update the hidden inputs in the main form
    if (sexTarget) sexTarget.value = document.getElementById('modal-sex-select').value;
    if (dobTarget) dobTarget.value = document.getElementById('modal-dob-input').value;
});