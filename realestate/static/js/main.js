const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

var url = $(location).attr('pathname');

if(!url.includes('register') && !url.includes('login')){
    setTimeout(function() {
        $('#message').fadeOut('slow');
    }, 5000);
}
// setTimeout(function() {
//     $('#message').fadeOut('slow');
// }, 5000);