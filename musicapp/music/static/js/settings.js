$(document).ready(function () {
  function follow(me, who) {
    let Url = "/api/follow/" + me;
    let csrf = localStorage.getItem("csrf");
    $.ajax({
      type: "POST",
      url: Url,
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrf);
        }
      },
      data: {
        csrfmiddlewaretoken: csrf,
        who: parseInt(who),
      },
      dataType: "json",
      success: function (response) {
        console.log(response);
      },
    });
  }
  function unfollow(me, who) {
    let Url = "/api/unfollow/" + me;
    let csrf = localStorage.getItem("csrf");
    $.ajax({
      type: "DELETE",
      url: Url,
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrf);
        }
      },
      data: {
        csrfmiddlewaretoken: csrf,
        who: who,
      },
      dataType: "json",
      success: function (response) {
        console.log(response);
      },
    });
  }

  function attachSong(songinfo) {
    let template = `
                    <tr scope="row" data-id=${songinfo.songid} data-is='unchecked'>
                      <td class="col-lg-1 col-2 col-sm-1" data-hint='songid'>${songinfo.songid}</td>
                      <td class='col-lg-1 col-2 col-sm-1 d-none' data-hint='isselect'><i
                              class="far fa-square fa-lg"></i></td>
                      <td class="col-lg-8 col-8 col-sm-8" data-hint='title'>${songinfo.songTitle}</td>
                      <td class="col-lg-2 col-2 col-sm-2 d-none d-sm-block" data-hint='duration'>
                          ${songinfo.songDuration}</td>
                      <td class='col-lg-1 col-2 col-sm-1 text-center' data-hint='favorite'><i
                              class="far fa-heart fa-lg text-danger"></i>
                      </td>
                    </tr>
      `;
    $("#songcontent").append(template);
  }

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  /* --------------------------------------------------- */

  $('[data-toggle="tooltip"]').tooltip();
  $("#addsong").fileinput({
    theme: "fas",
    uploadUrl:
      "http://localhost:8000/api/addsong/" + localStorage.getItem("uid"),
    uploadExtraData: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      uid: localStorage.getItem("uid"),
    },
    allowedFileTypes: ["audio"],
    allowedFileExtensions: ["mp3", "ogg", "wav"],
    ajaxSettings: {
      success: function (data) {
        if (data.Already == "!EXIST") {
          attachSong(data.songinfo);
        }
      },
    },
    mergeAjaxCallbacks: [true, "after"],
  });
  $(".file-preview-thumbnails").slimscroll();
  window.selectortoggled = false;
  window.selectall = false;
  window.selectcount = 0;
  $("#songselector").on("click", function (e) {
    let ts1, ts2, th1, th2;
    if (window.selectortoggled === true) {
      ts1 = $("th[data-hint=songidHead]");
      ts2 = $("td[data-hint=songid]");
      th1 = $("th[data-hint=selector]");
      th2 = $("td[data-hint=isselect]");
      $(".songoptions").hide();
    } else {
      th1 = $("th[data-hint=songidHead]");
      th2 = $("td[data-hint=songid]");
      ts1 = $("th[data-hint=selector]");
      ts2 = $("td[data-hint=isselect]");
      $(".songoptions").show();
    }
    ts1.removeClass("d-none");
    th1.addClass("d-none");
    ts2.removeClass("d-none");
    th2.addClass("d-none");
    if (window.selectortoggled === false) {
      ts1.on("click", function (e) {
        let select;
        if (selectall === false) {
          ts1.find("i").removeClass("fa-square");
          ts1.find("i").addClass("fa-check-square");
          select = ts2.find("i.fa-square");
          select.parent().parent().attr("data-is", "checked");
          select.removeClass("fa-square");
          select.addClass("fa-check-square");
        } else {
          ts1.find("i").removeClass("fa-check-square");
          ts1.find("i").addClass("fa-square");
          select = ts2.find("i.fa-check-square");
          select.parent().parent().attr("data-is", "unchecked");
          select.removeClass("fa-check-square");
          select.addClass("fa-square");
        }
        window.selectcount = $("tr[data-is=checked]").length;
        if (window.selectall === true) {
          window.selectall = false;
        } else {
          window.selectall = true;
        }
      });
      $("td[data-hint=isselect]").on("click", function (e) {
        let self = $(e.target);
        let parent = self.parent().parent();
        if (parent.attr("data-is") == "unchecked") {
          self.removeClass("fa-square");
          self.addClass("fa-check-square");
          parent.attr("data-is", "checked");
        } else {
          self.removeClass("fa-check-square");
          self.addClass("fa-square");
          parent.attr("data-is", "unchecked");
        }
        window.selectcount = $("tr[data-is=checked]").length;
      });
    } else {
      th1.on("click", function (e) {
        let select;
        if (selectall === false) {
          th1.find("i").removeClass("fa-square");
          th1.find("i").addClass("fa-check-square");
          select = th2.find("i.fa-square");
          select.parent().parent().attr("data-is", "checked");
          select.removeClass("fa-square");
          select.addClass("fa-check-square");
        } else {
          th1.find("i").removeClass("fa-check-square");
          th1.find("i").addClass("fa-square");
          select = th2.find("i.fa-check-square");
          select.parent().parent().attr("data-is", "unchecked");
          select.removeClass("fa-check-square");
          select.addClass("fa-square");
        }
        window.selectcount = $("tr[data-is=checked]").length;
        if (window.selectall === true) {
          window.selectall = false;
        } else {
          window.selectall = true;
        }
      });
    }
    window.selectcount = $("tr[data-is=checked]").length;
    if (window.selectortoggled === true) {
      window.selectortoggled = false;
    } else {
      window.selectortoggled = true;
    }
  });
  $("#plistselector").on("click", function (e) {
    let ts1, ts2, th1, th2;
    if (window.selectortoggled === true) {
      ts1 = $("th[data-hint=plistidHead]");
      ts2 = $("td[data-hint=plistid]");
      th1 = $("th[data-hint=selector]");
      th2 = $("td[data-hint=isselect]");
      $(".plistoptions").hide();
    } else {
      th1 = $("th[data-hint=plistidHead]");
      th2 = $("td[data-hint=plistid]");
      ts1 = $("th[data-hint=selector]");
      ts2 = $("td[data-hint=isselect]");
      $(".plistoptions").show();
    }
    ts1.removeClass("d-none");
    th1.addClass("d-none");
    ts2.removeClass("d-none");
    th2.addClass("d-none");
    if (window.selectortoggled === false) {
      ts1.on("click", function (e) {
        let select;
        if (selectall === false) {
          ts1.find("i").removeClass("fa-square");
          ts1.find("i").addClass("fa-check-square");
          select = ts2.find("i.fa-square");
          select.parent().parent().attr("data-is", "checked");
          select.removeClass("fa-square");
          select.addClass("fa-check-square");
        } else {
          ts1.find("i").removeClass("fa-check-square");
          ts1.find("i").addClass("fa-square");
          select = ts2.find("i.fa-check-square");
          select.parent().parent().attr("data-is", "unchecked");
          select.removeClass("fa-check-square");
          select.addClass("fa-square");
        }
        window.selectcount = $("tr[data-is=checked]").length;
        if (window.selectall === true) {
          window.selectall = false;
        } else {
          window.selectall = true;
        }
      });
      $("td[data-hint=isselect]").on("click", function (e) {
        let self = $(e.target);
        let parent = self.parent().parent();
        if (parent.attr("data-is") == "unchecked") {
          self.removeClass("fa-square");
          self.addClass("fa-check-square");
          parent.attr("data-is", "checked");
        } else {
          self.removeClass("fa-check-square");
          self.addClass("fa-square");
          parent.attr("data-is", "unchecked");
        }
        window.selectcount = $("tr[data-is=checked]").length;
      });
    } else {
      th1.on("click", function (e) {
        let select;
        if (selectall === false) {
          th1.find("i").removeClass("fa-square");
          th1.find("i").addClass("fa-check-square");
          select = th2.find("i.fa-square");
          select.parent().parent().attr("data-is", "checked");
          select.removeClass("fa-square");
          select.addClass("fa-check-square");
        } else {
          th1.find("i").removeClass("fa-check-square");
          th1.find("i").addClass("fa-square");
          select = th2.find("i.fa-check-square");
          select.parent().parent().attr("data-is", "unchecked");
          select.removeClass("fa-check-square");
          select.addClass("fa-square");
        }
        window.selectcount = $("tr[data-is=checked]").length;
        if (window.selectall === true) {
          window.selectall = false;
        } else {
          window.selectall = true;
        }
      });
    }
    window.selectcount = $("tr[data-is=checked]").length;
    if (window.selectortoggled === true) {
      window.selectortoggled = false;
    } else {
      window.selectortoggled = true;
    }
  });

  $("#songtoplist").on("click", function () {
    if (window.selectcount > 0) {
      $(this).attr("data-target", "#toplistmodal");
      window.selectedsonglist = [];
      $("tr[data-is=checked]").each(function () {
        window.selectedsonglist.push(parseInt($(this).attr("data-id")));
      });
    } else {
      $(this).attr("data-target", "");
    }
  });

  $("#deletesong").on("click", function () {
    if (window.selectcount > 0) {
      $("#deletemsgbox").html(
        window.selectcount + " songs selected. Are you sure ?"
      );
      $(this).attr("data-target", "#deletesongmodal");
      window.selectedsonglist = [];
      $("tr[data-is=checked]").each(function () {
        window.selectedsonglist.push(parseInt($(this).attr("data-id")));
      });
    } else {
      $(this).attr("data-target", "");
    }
  });
  $("#submitsongtoplaylist").on("click", function () {
    let playlistid = $("select[name=plist]").val();
    let csrf = $("input[name=csrfmiddlewaretoken]").val();
    let Url =
      "/api/updateplaylist/" + localStorage.getItem("uid") + "/" + playlistid;
    $.ajax({
      type: "PUT",
      url: Url,
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrf);
        }
      },
      data: {
        csrfmiddlewaretoken: csrf,
        changename: false,
        plistId: playlistid,
        songIds: `${window.selectedsonglist}`,
      },
      dataType: "json",
      success: function (response) {
        if (response.songsadded.length > 0) {
          $("#songToast>.toast-header").html(
            '<a href="#" class="btn btn-info">Success</a>'
          );
          $("#songToast>.toast-body").html(
            "<p>" +
              response.songsadded.length +
              " songs added to " +
              response.playlistname +
              "</p>"
          );
          $("#songToast").toast({
            animation: true,
            delay: 3000,
          });
          $("#songToast").toast("show");
        } else {
          $("#songToast>.toast-header").html(
            '<a href="#" class="btn btn-info">Oopsi!</a>'
          );
          $("#songToast>.toast-body").html(
            "<p><strong>" + (response.msg.length > 1)
              ? response.msg.length +
                  " songs already exist in " +
                  response.playlistname
              : response.msg[0] + "</strong></p>"
          );
          $("#songToast").toast({
            animation: true,
            delay: 3000,
          });
          $("#songToast").toast("show");
        }
      },
    });
  });
  $("#confirmSongDelete").on("click", function () {
    let csrf = $("input[name=csrfmiddlewaretoken]").val();
    for (songid of window.selectedsonglist) {
      let Url = "/api/deletesong/" + localStorage.getItem("uid") + "/" + songid;
      $.ajax({
        type: "DELETE",
        url: Url,
        beforeSend: function (xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
          }
        },
        data: {
          csrfmiddlewaretoken: csrf,
        },
        dataType: "json",
        success: function (response) {
          $("tr[data-id=" + response.deletedsongid + "]").remove();
        },
      });
    }
    $(".close").click();
  });
  $("#confirmPlistSongDelete").on("click", function () {
    let csrf = $("input[name=csrfmiddlewaretoken]").val();
    for (sid of window.selectedplaylistsongs) {
      let Url =
        "/api/deleteplaylistsong/" +
        localStorage.getItem("uid") +
        "/" +
        localStorage.getItem("pid") +
        "/" +
        sid;
      $.ajax({
        type: "DELETE",
        url: Url,
        beforeSend: function (xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
          }
        },
        data: {
          csrfmiddlewaretoken: csrf,
        },
        dataType: "json",
        success: function (response) {
          $("tr[data-id=" + response.deletedplaylistsongid + "]").remove();
        },
      });
    }
    $(".close").click();
  });

  $("#confirmPlistDelete").on("click", function () {
    let csrf = $("input[name=csrfmiddlewaretoken]").val();
    for (pid of window.selectedplaylist) {
      let Url =
        "/api/deleteplaylist/" + localStorage.getItem("uid") + "/" + pid;
      $.ajax({
        type: "DELETE",
        url: Url,
        beforeSend: function (xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
          }
        },
        data: {
          csrfmiddlewaretoken: csrf,
        },
        dataType: "json",
        success: function (response) {
          $("tr[data-id=" + response.deletedplaylistid + "]").remove();
        },
      });
    }
    $(".close").click();
  });

  $("#deleteplist").on("click", function () {
    if (window.selectcount > 0) {
      $("#deletemsgbox").html(
        window.selectcount + " playlist selected. Are you sure ?"
      );
      $(this).attr("data-target", "#deleteplistmodal");
      window.selectedplaylist = [];
      $("tr[data-is=checked]").each(function () {
        window.selectedplaylist.push(parseInt($(this).attr("data-id")));
      });
    } else {
      $(this).attr("data-target", "");
    }
  });

  $("#deleteplistsongs").on("click", function () {
    if (window.selectcount > 0) {
      $("#deletepsongmsgbox").html(
        window.selectcount + " songs selected. Are you sure ?"
      );
      $(this).attr("data-target", "#deleteplistsongmodal");
      window.selectedplaylistsongs = [];
      $("tr[data-is=checked]").each(function () {
        window.selectedplaylistsongs.push(parseInt($(this).attr("data-id")));
      });
    } else {
      $(this).attr("data-target", "");
    }
  });

  $(".follow").on("click", function () {
    p = $(this).parents("[class=card]");
    follow(localStorage.getItem("uid"), p.attr("uid"));
  });

  $(".unfollow").on("click", function () {
    p = $(this).parents("[class=card]");
    unfollow(localStorage.getItem("uid"), p.attr("uid"));
  });
});
