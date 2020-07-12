$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip({
    html: true,
  });
  $(".toast").toast({
    animation: true,
    delay: 1000,
  });
  $(".toast").toast("show");
});
