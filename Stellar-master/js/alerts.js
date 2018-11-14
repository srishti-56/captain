var global = -1;
(function($) {
  showSwal = function(type,iden){
        'use strict';
        if(type === 'basic'){
        	swal({
            text: 'Any fool can use a computer',
            button: {
              text: "OK",
              value: true,
              visible: true,
              className: "btn btn-primary"
            }
          })

    	}else if(type === 'success-message'){
        swal({
          title: 'Congratulations!',
          text: 'You entered the correct answer',
          icon: 'success',
          button: {
            text: "Continue",
            value: true,
            visible: true,
            className: "btn btn-primary"
          }
        })

    	}else if(type === 'warning-message-and-cancel'){
            swal({
              title: 'Are you sure?',
              text: "You won't be able to revert this!",
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3f51b5',
              cancelButtonColor: '#ff4081',
              confirmButtonText: 'Great ',
              buttons: {
                cancel: {
                  text: "Cancel",
                  value: null,
                  visible: true,
                  className: "btn btn-danger",
                  closeModal: true,
                },
                confirm: {
                  text: "OK",
                  value: true,
                  visible: true,
                  className: "btn btn-primary",
                  closeModal: true
                  
                }
              }
            })
            .then((value) => {
              if(value == true)
              {
                swal( {title: 'Congratulations!',
                text: 'Sent to the teacher for approval :)',
                icon: 'success'});
                
              }

              
              

            })
            $(iden).remove();
            


    	}
        }
      

})
(jQuery);
