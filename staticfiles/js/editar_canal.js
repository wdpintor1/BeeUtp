$(document).ready(function() {
     // Función para manejar la validación cuando cambia el estado del checkbox
     $(".activo-campo-input").change(function () {
        var prefix = $(this).attr("id").replace("id_activo_campo_adicional_", "");
        var nombreInput = $("#" + prefix + "-nombre");

        // Si el checkbox está marcado, haz que el nombre sea requerido
        if ($(this).prop("checked")) {
            nombreInput.prop("readonly", false);
            nombreInput.prop("required", true);
        } else {
            nombreInput.prop("readonly", true);
            nombreInput.prop("required", false);
        }
    });
});