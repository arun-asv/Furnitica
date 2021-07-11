$(document).ready(function(){
    $("#customerForm").validate({

    rules:{
        firstname: {
            required: true,
            minlength: 3

        },

        lastname: {
            required: true,
            minlength: 3
        },

        username: {
            required: true,
            minlength: 6

    },
        email: {
            required: true,
            email: true
        },

        password1: {
            required: true,
            minlength: 4,

        },

        password2: {
            required: true,
            minlength: 4,
            equalTo: "#password1"
        },

        number : {
            required: true,
            minlength: 10,
            maxlength: 10,
            digits: true
        }

},
    messages: {
        firstname: {
            required: "Please enter your firstname",
            minlength: "Enter at least 3 characters"
        },

        lastname: {
            required: "Please enter your lastname",
            minlength: "Enter at least 3 characters"
        },

        username: {
            required: "Please enter a username",
            minlength: "Enter at least 6 characters"


        },

        email: {
            required: "Please enter your email",
            email: "Enter a valid email"
        },

        number:{
            required: "Please enter your mobile number",
            digits: "Enter a valid phone number",
            minlength: "Enter a valid phone number",
            maxlength: "Enter a valid phone number"
        }


    }


    })



})

