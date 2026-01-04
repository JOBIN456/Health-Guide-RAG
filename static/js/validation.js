$(document).ready(function () {
    $("#RegisterForm").validate({
      rules: {
        username: {
          required: true,
          minlength: 3
        },
        password1: {
          required: true,
          minlength: 6
        },
        password2: {
          required: true,
          equalTo: "#password1"
        }
      },
      messages: {
        username: {
          required: "Please enter your username",
          minlength: "Username must be at least 3 characters"
        },
        password1: {
          required: "Please enter a password",
          minlength: "Password must be at least 6 characters"
        },
        password2: {
          required: "Please confirm your password",
          equalTo: "Passwords do not match"
        }
      },
      submitHandler: function (form) {
        // AJAX submission
        $.ajax({
          type: "POST",
          url: "/registersubmit/",
          data: {
            username: $("#username").val(),
            password1: $("#password1").val(),
            password2: $("#password2").val(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
          },
          success: function (response) {
            Swal.fire({
                icon: 'success',
                title: 'Success!',
                text: response.message,
                showConfirmButton: false,
                timer: 1500
            }).then(() => {
                window.location.href = response.redirect;  // ✅ Correct way to redirect
            });
            $("#RegisterForm")[0].reset(); // Clear the form
        },
          error: function (xhr) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: xhr.responseJSON?.message || "Something went wrong"
              });
              $("#RegisterForm")[0].reset(); // Clear the form

          }
        });
      }
    });




// LOGIN VALIDATION

    $("#loginform").validate({
        rules: {
          username: {
            required: true
          },
          password: {
            required: true
          }
        },
        messages: {
          username: "Please enter your username",
          password: "Please enter your password"
        },
        submitHandler: function (form) {
          $.ajax({
            type: "POST",
            url: "/loginsubmit/",
            data: {
              username: $("#username").val(),
              password: $("#password").val(),
              csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            beforeSend: function () {
              $(".btnglasss").prop("disabled", true).text("Logging in...");
            },
            success: function (response) {
              Swal.fire({
                icon: 'success',
                title: 'Welcome!',
                text: response.message
              }).then(() => {
                window.location.href = response.redirect;  // ✅ Correct way to redirect
            });
              $("#loginform")[0].reset();
            },
            error: function (xhr) {
              Swal.fire({
                icon: 'error',
                title: 'Login Failed',
                text: xhr.responseJSON?.message || "Something went wrong"
              });
              $("#loginform")[0].reset();

            },
            complete: function () {
              $(".btnglasss").prop("disabled", false).text("Login");
            }
          });
        }
      });




  });










