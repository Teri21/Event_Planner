// $(document).ready(function(){

    $('#createEvent').submit(function (e) { 
        e.preventDefault();
        console.log(e)
        console.log(this);

        $.ajax({        
            url: "/create_event",
            method: 'post',
            data: $(this).serialize(),        
            success: function (serverResponse) {
                console.log("this is ajax working");
                console.log(serverResponse);
                $('.all_events').prepend(serverResponse);
            }
        });
    });
    
// });