$(document).ready(function() {
    const nickColor = $("#nick_color"),
          nickText = $("#nick_text"),
          sexValue = $(".sexs input[type='radio']"),
          savedNickColor = localStorage.getItem("nickColor");
          savedNickText = localStorage.getItem("nickText");
          savedSexValue = localStorage.getItem("sexValue");

    if (savedNickColor) {
        nickColor.val(savedNickColor);
    }

    if (savedNickText) {
        nickText.val(savedNickText);
    }

    if (savedSexValue) {
        $(`.sexs input[value="${savedSexValue}"]`).prop("checked", true);
    }

    nickColor.on("change", function() {
        localStorage.setItem("nickColor", nickColor.val());
    });

    nickText.on("input", function() {
        localStorage.setItem("nickText", nickText.val());
    });

    sexValue.on("change", function() {
        localStorage.setItem("sexValue", $(this).val());
    });
});