$(document).on('click', '#del-catgory', function(){
    var category_id = $(this).data('category-id')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    

    swal({
        title: "Are You sure",
        text:"Do you want to delete this category???",
        icon:"warning",
        buttons: ["cancel", "Delete"],
        dangerMode: true,
    }).then(function(confirmDelete){
        if (confirmDelete) {
            $.ajax({
                url:"/adminn/del-category/",
                method:"POST",
                data:{
                    'category_id':category_id,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:"Deleted",
                        text:response.message,
                        icon:"success",
                        timer:4000,
                        button:false,
                    }).then(function() {
                        $("#category-block").load(location.href + ' #category-block');
                    });
                } 
            })
        }
    });

    
    
});



// product form

// $(document).ready(function() {
//     var imageFields = $('#image-fieldd');
//     var addButton   = $('#add-image-butn');

//     addButton.on('click', function() {
//         var newImageField = $('<p>{{image_form.image.label_tag}} {{image_form.image}}</p>');
//         imageFields.append(newImageField)
//     })
// });


//delete product

$(document).on('click', '#del-product', function(){
    var product_id = $(this).data('product-id')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    

    swal({
        title: "Are You sure",
        text:"Do you want to delete this Product???",
        icon:"warning",
        buttons: ["cancel", "Delete"],
        dangerMode: true,
    }).then(function(confirmDelete){
        if (confirmDelete) {
            $.ajax({
                url:"/adminn/del-product/",
                method:"POST",
                data:{
                    'product_id':product_id,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:"Deleted",
                        text:response.message,
                        icon:"success",
                        timer:4000,
                        button:false,
                    }).then(function() {
                        $("#pro-tab-body").load(location.href + ' #pro-tab-body');
                    });
                } 
            })
        }
    });

    
    
});


// deactivate product

$(document).on('click', '#deact-product', function(){
    var product_id = $(this).data('product-id')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    var text = $(this).text()


    swal({
        title: "Are You sure",
        text:'Do you want to '+ text +' this Product???',
        icon:"warning",
        buttons: ["cancel", "Confirm"],
        dangerMode: true,
    }).then(function(confirmConfirm){
        if (confirmConfirm) {
            $.ajax({
                url:"/adminn/deact-product/",
                method:"POST",
                data:{
                    'product_id':product_id,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:response.title,
                        text:response.message,
                        icon:"success",
                        timer:4000,
                        button:false,
                    }).then(function() {
                        $("#pro-tab-body").load(location.href + ' #pro-tab-body');
                    });
                } 
            })
        }
    });

    
    
});


//Delete product

$(document).on('click', '#prod-var-del', function() {
    var product_var_id = $(this).data('productvariation-id')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    

    swal({
        title:"Are You Sure",
        text:"Do you want to delete this variation!!",
        icon:"warning",
        buttons:['cancel', 'Delete'],
        dangerMode:true,
    }).then(function(confirmDelete){
        if (confirmDelete) {
            $.ajax({
                url:"/adminn/ad-del-product-variations/",
                method:"POST",
                data:{
                    'product_var_id':product_var_id,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:'Deleted',
                        text:response.message,
                        icon:"success",
                        timer:4000,
                        button:false,
                    }).then(function(){
                        $("#pro-var-block").load(location.href + ' #pro-var-block')
                    })
                }
            })
        }
    })
})


$(document).on('click' ,'#prod-var-deact', function() {

    var product_var_id = $(this).data('productvariation-id')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    var text = $(this).text()
    console.log('text : ', text)
    swal({
        title:"Are you sure",
        text:'Do you want to '+ text +' this Variation ???',
        icon:'warning',
        buttons:['Cancel', 'Confirm'],
        dangerMode:true,

    }).then(function(confirmConfirm){
        if (confirmConfirm) {
            $.ajax({
                url:"/adminn/ad-deact-product-variations/",
                method:"POST",
                data:{
                    'product_var_id':product_var_id,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response) {
                    swal({
                        title:response.title,
                        text:response.message,
                        icon:'success',
                        timer:4000,
                        button:false,
                    }).then(function() {
                        $('#pro-var-block').load(location.href + ' #pro-var-block')
                    })
                }
            }) 
        }
    })

})

// Delete brand

$(document).on('click', '#del-brand', function() {
    var brand_id = $(this).data('brand-id')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()

    swal({
        title:"Are You Sure",
        text:"Do you want to delete this brand???",
        icon:'warning',
        buttons:['Cancel', 'Delete'],
        dangerMode:true,
    }).then(function(confirmDelete){
        if(confirmDelete) {
            $.ajax({
                url:"/adminn/ad-del-brand/",
                method:"POST",
                data:{
                    'brand_id':brand_id,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:"Deleted",
                        text:response.message,
                        icon:'success',
                        timer:4000,
                        button:false,
                        
                    }).then(function() {
                        $('#brand-block').load(location.href + ' #brand-block')
                    })
                }
                
            })
        }
    })
})

// status change for admin

function statusChange(orderItemId, status) {
    console.log('order item id : ', orderItemId)
    console.log('status : ', status)
    swal({
        title:"Are You Sure!",
        text:"Do you Want to change the status of the order",
        icon:"warning",
        buttons:['Cancel','Yes'],
    }).then(function(confirmYes) {
        if(confirmYes){
            $.ajax({
                url:"/adminn/ad-status-update/",
                data:{
                    'orderproduct_id':orderItemId,
                    'status':status,
                },
                success:function(response){
                    swal({
                        title:"Updated",
                        text:response.message,
                        icon:"success",
                        timer:4000,
                        button:false,
                    }).then(function(){
                        $('#order-block').load(location.href + ' #order-block')
                    })
                }
            })
        }
    })

}



// Delete Coupon

$(document).on('click', '#delCoupon', function() {
    var coupon_id = $(this).data('coupon-id')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    swal({
        title:"Are You Sure",
        text:"Do you want to delete this Coupon ???",
        icon:'warning',
        buttons:['Cancel', 'Delete'],
        dangerMode:true,
    }).then(function(confirmDelete){
        if(confirmDelete) {
            $.ajax({
                url:"/adminn/ad-del-coupon/",
                method:"POST",
                data:{
                    'coupon_id':coupon_id,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:"Deleted",
                        text:response.message,
                        icon:'success',
                        timer:4000,
                        button:false,
                        
                    }).then(function() {
                        $('#couponBlock').load(location.href + ' #couponBlock')
                    })
                }
                
            })
        }
    })
})



// deactivate Coupon

$(document).on('click', '#coupon-deact', function(){
    var coupon_id = $(this).data('coupon-id')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    var text = $(this).text()


    swal({
        title: "Are You sure",
        text:'Do you want to '+ text +' this Coupon???',
        icon:"warning",
        buttons: ["cancel", "Confirm"],
        dangerMode: true,
    }).then(function(confirmConfirm){
        if (confirmConfirm) {
            $.ajax({
                url:"/adminn/deact-coupon/",
                method:"POST",
                data:{
                    'coupon_id':coupon_id,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:response.title,
                        text:response.message,
                        icon:"success",
                        timer:4000,
                        button:false,
                    }).then(function() {
                        $("#couponBlock").load(location.href + ' #couponBlock');
                    });
                } 
            })
        }
    });

    
    
});


// deactivate User

$(document).on('click', '#user-deact', function(){
    var user_id = $(this).data('user-id')
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    var text = $(this).text()


    swal({
        title: "Are You sure",
        text:'Do you want to '+ text +' this User???',
        icon:"warning",
        buttons: ["cancel", "Confirm"],
        dangerMode: true,
    }).then(function(confirmConfirm){
        if (confirmConfirm) {
            $.ajax({
                url:"/adminn/deact-user/",
                method:"POST",
                data:{
                    'user_id':user_id,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:response.title,
                        text:response.message,
                        icon:"success",
                        timer:4000,
                        button:false,
                    }).then(function() {
                        $("#usertableBlock").load(location.href + ' #usertableBlock');
                    });
                } 
            })
        }
    });

    
    
});