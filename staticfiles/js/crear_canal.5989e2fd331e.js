$(document).ready(function () {
    $('.activo-campo-input').change(function () {
        var index = $('.activo-campo-input').index(this);
        $('.campo-adicional-input').eq(index).prop('readonly', !$(this).prop('checked'));
    });

    // Deshabilitar los campos que estén desactivados inicialmente
    $('.activo-campo-input:not(:checked)').each(function () {
        var index = $('.activo-campo-input').index(this);
        $('.campo-adicional-input').eq(index).prop('readonly', true);
    });
    // Escuchar cambios en los checkboxes
    $(":checkbox").change(function () {
        var campoId = $(this).attr("id").replace("id_activo_campo_adicional_", "");
        var inputCampo = $("#id_campo_adicional_" + campoId);

        // Establecer o quitar el atributo 'required' según el estado del checkbox
        if ($(this).is(":checked")) {
            inputCampo.prop("readonly", false);
            inputCampo.prop("required", true);
        } else {
            inputCampo.prop("readonly", true);
            inputCampo.prop("required", false);
        }
    });
});