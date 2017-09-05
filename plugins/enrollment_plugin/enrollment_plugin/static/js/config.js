$(document).ready(function() {
    $("#btn_back").click(function() {
        $("#config_wizard").hide();
        $("#config_home").show();
    });

    $("#btn_save").click(function() {
       if (confirm("Are you sure you want to save?")) {
           var to_send = {
               "id": $("#span_id").html(),
               "name": $("#tb_name").val(),
               "open_date": $("#dp_open").val(),
               "close_date": $("#dp_close").val(),
               "expires": $("#cb_expires").val(),
               "expiry_date": $("#dp_expires").val(),
               "plugin_id": $("#plugin_id").html()
           };

           $.ajax(
               {
                   url: "/metadata",
                   method: "POST",
                   data: to_send,
                   success: function() {
                       // noinspection SillyAssignmentJS
                       document.location.href = document.location.href;
                   },
                   fail: function() {
                       alert("Error occurred on saving of enrollment");
                   }
               }
           )
       }
    });

    $("#cb_expires").change(function(){
        if ($(this).is(":checked")) {
            $("#dp_expires").prop("disabled", false);
        } else {
            $("#dp_expires").prop("disabled", true);
        }
    });

    $("#btn_new_enrollment").click(function(){
        prepare_wizard_new();
    });
});

function show_metadata(enrollment_id) {
    $.ajax(
        {
            url: "/metadata?enrollment_id=" + enrollment_id,
            method: "GET",
            dataType: "json",
            success: function(data) {
                alert(data);
                prepare_wizard_existing(data);
                $("#config_home").hide();
                $("#config_wizard").show();
            },
            fail: function() {
                alert("Metadata retrieval failed");
            }
        }
    );
}

function remove_enrollment(enrollment_id) {

    var to_send = {
        "plugin_id": $("#plugin_id").html(),
        "id": $("#span_id").html()
    };

    if (confirm("Removing enrollments will remove all participants in enrollment and any associated surveys")) {
        $.ajax({
            url: "/metadata",
            data: to_send,
            method: "DELETE",
            success: function() {
                // noinspection SillyAssignmentJS
                document.location.href = document.location.href;
            },
            fail: function() {
                alert("Error occurred on removal of enrollment");
            }
        });
    }
}

function prepare_wizard_new() {
    $("#span_id").html("<em>Generated on save</em>");
    $("#span_url").html("<em>Generated on save</em>");
    $("#tb_name").val("");
    $("#dp_open").val("");
    $("#dp_close").val("");
    $("#cb_expires").prop('checked', false);
    $("#dp_expires").val("").prop('disabled', true);
}

function prepare_wizard_existing(enrollment) {
    $("#span_id").html(enrollment["id"]);
    $("#span_url").html(enrollment["url"]);
    $("#tb_name").val(enrollment["name"]);
    $("#dp_open").val(enrollment["open_date"]);
    $("#dp_close").val(enrollment["close_date"]);

    if (enrollment["expiry_date"] === '0') {
        $("#cb_expires").prop('checked', false);
        $("#dp_expires").val("").prop('disabled', true);
    } else {
        $("#cb_expires").prop('checked', true);
        $("#dp_expires").val(enrollment["expiry_date"]).prop('disabled', false);
    }
}

//TODO: THIS IS WHERE I LEFT OFF, SHOW META_DATA