(function ($) {
    console.log("hello")
    // FORM
    $('form').submit(function (event) {
        event.preventDefault();
        $('.preloader').fadeIn(500);
        const formData = new FormData(this);
        const requestData = JSON.stringify(Object.fromEntries(formData));
        console.log(requestData)
        const myHeaders = new Headers ();
        myHeaders.append("Content-Type", "application/json");
        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: requestData,
            redirect: 'follow'
        };
        fetch("https://6spc3pyri2doc7r7dfssj4upni0hloui.lambda-url.us-west-1.on.aws/", requestOptions)
            .then(response => response.text())
            .then(result => {
                if (result == 'Form submitted') {
                    alert('Message recieved. Will reply shortly.')
                } else {
                    alert(result)
                }
            })
            .catch(error => {
                alert('Error please trya again.')
            });
    });
}) (jQuery);

