$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();

  $("#addsong").fileinput({
    theme: "fas",
    uploadUrl: "http://localhost:8000/api/addsong/3",
    uploadExtraData: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
  });

  $(".file-preview-thumbnails").slimscroll();
});
