$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();
  $(".fancyupload").FancyFileUpload({
    accept: ["audio/ogg", "audio/mpeg"],
  });
});
