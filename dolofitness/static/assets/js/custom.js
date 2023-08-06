$(document).ready(function() {
    // $('#pro_form').submit(function(event) {
    //     event.preventDefault(); 
    //     var formData = new FormData(this);

    //     $.ajax({
    //         method:"POST",
    //         data:formData,
    //         processData:false,
    //         contentType:false,
    //         success: function(response) {

                

    //             $('#id_public_name').val(response.public_name)
    //             $('#pr-pic img').attr('src',response.profile_pic)
    //             swal({
    //                 title: "Success",
    //                 text: "Profile Updated!!",
    //                 icon: "success",
    //                 button: "OK",
    //             });

    //         },
    //     })
        
      
    // });

    
    // 31-07-2023

    $(document).on('submit', '#address-form', function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        

        $.ajax({
            method:"POST",
            data:formData,
            processData:false,
            contentType:false,
            success:function(response){
                $('#newAddressModal').modal('hide');
                swal({
                    title:response.title,
                    text:response.text,
                    icon:response.icon,
                    timer:4000,
                    button:false,

                }).then(function(){
                    $('#address-block').load(location.href + ' #address-block', function(){
                        $(document).on('click', '#newAdd', function() {
                            $('#newAddressModal').modal('show');
                        });
                    });
                });
                
            }
        })

    });

    // check address form submission

    $(document).on('submit', '#check-address-form', function(e) {
        e.preventDefault();
        console.log('check address submission ')
        var formData = new FormData(this);
        

        $.ajax({
            method:"POST",
            url:'/my-address/',
            data:formData,
            processData:false,
            contentType:false,
            success:function(response){
                $('#newAddressModal').modal('hide');
                swal({
                    title:response.title,
                    text:response.text,
                    icon:response.icon,
                    timer:4000,
                    button:false,

                }).then(function(){
                    $('#address-block').load(location.href + ' #address-block', function(){
                        $(document).on('click', '#newAdd', function() {
                            $('#newAddressModal').modal('show');
                        });
                    });
                });
                
            }
        })

    });




    //Edit address-------------------

    $(document).on('click', '#edit-buton', function(e){
        e.preventDefault();
        // console.log('edit button')
        var addressId = $(this).closest('.col-lg-6').data('address-id')
        // console.log('address id : ',addressId)

        $.ajax({
            method:"GET",
            url:'/get-address/' + addressId,
            success:function(response){
                // console.log('response : ',response)
                var addressData = response
                $('#address-form input[name="first_name"]').val(addressData.first_name);
                $('#address-form input[name="last_name"]').val(addressData.last_name);
                $('#address-form input[name="email"]').val(addressData.email);
                $('#address-form input[name="address_line1"]').val(addressData.address_line1);
                $('#address-form input[name="address_line2"]').val(addressData.address_line2);
                $('#address-form input[name="phone"]').val(addressData.phone);
                $('#address-form input[name="city"]').val(addressData.city);
                $('#address-form input[name="state"]').val(addressData.state);
                $('#address-form input[name="country"]').val(addressData.country);
                $('#address-form input[name="postcode"]').val(addressData.postcode);
                
                $('#newAddressModalLabel').text('Edit Address');

                //hidden field
                $('#addr_id_input').val(addressId)

                $('#newAddressModal').modal('show');
            },
            error:function(xhr, status, error) {
                console.log('Error retrieving address data : ',error);
            }
        })
    });

    // test 

    $(document).on('click', '#edit-check-buton', function(e){
        e.preventDefault();
        console.log('edit button')
        var addressId = $(this).closest('.col-lg-6').data('address-id')
        console.log('address id : ',addressId)

        $.ajax({
            method:"GET",
            url:'/get-address/' + addressId,
            success:function(response){
                // console.log('response : ',response)
                var addressData = response
                $('#check-address-form input[name="first_name"]').val(addressData.first_name);
                $('#check-address-form input[name="last_name"]').val(addressData.last_name);
                $('#check-address-form input[name="email"]').val(addressData.email);
                $('#check-address-form input[name="address_line1"]').val(addressData.address_line1);
                $('#check-address-form input[name="address_line2"]').val(addressData.address_line2);
                $('#check-address-form input[name="phone"]').val(addressData.phone);
                $('#check-address-form input[name="city"]').val(addressData.city);
                $('#check-address-form input[name="state"]').val(addressData.state);
                $('#check-address-form input[name="country"]').val(addressData.country);
                $('#check-address-form input[name="postcode"]').val(addressData.postcode);
                
                $('#newAddressModalLabel').text('Edit Address');

                //hidden field
                $('#addr_id_input').val(addressId)

                $('#newAddressModal').modal('show');
            },
            error:function(xhr, status, error) {
                console.log('Error retrieving address data : ',error);
            }
        })
    });


    


    // Delete address


    // $(document).on('click', '#del-buton', function(e){
    //     e.preventDefault()
    //     var addressId = $(this).closest('.col-lg-6').data('address-id');

    //     swal({
    //         title:"Are You Sure",
    //         text:"Do you want delete this address??",
    //         icon:"warning",
    //         buttons: ["Cancel", "Delete"],
    //         dangerMode: true,
    //     }).then(function(confirmDelete){
    //         if (confirmDelete) {
            
    //             $.ajax({
    //                 method:"GET",
    //                 url:'/delete-address/' + addressId,
    //                 success:function(response){
    //                     swal({
    //                         title:"Deleted",
    //                         text:"Address Deleted!",
    //                         icon:"success",
    //                         timer:4000,
    //                         button:false,
    //                     }).then(function(){
    //                         $('#address-block').load(location.href + ' #address-block');
    //                     });
    //                 }
    //             })
    //         }
    //     });
    // });


    //set default address
    $(document).on('click', '#default-buton', function(e){
        e.preventDefault();
        console.log('default button pressed..')
        var addressId = $(this).closest('.col-lg-6').data('address-id')
        console.log('address id : ',addressId)

        $.ajax({
            method:"GET",
            url:"/set-default-address/" + addressId,
            success:function(response){
                console.log("response : ", response)
                $('#address-block').load(location.href + ' #address-block');
            }
        })
    });



    //Get weight

    // $('select[name="flavor"]').change(function () {
    //     var flavor = $(this).val()
    //     console.log('flavor : ',flavor)

    //     $.ajax({
    //         method:'GET',
    //         url:'/shop/get-weight/',
    //         data:{
    //             'flavor':flavor,
    //         },
    //         success:function(response){
    //             console.log('response :',response)
    //         }
    //     })
        
    // })

});



//
$(document).on('click', '#newAdd', function(e){
    e.preventDefault();
    

    // Reset the form fields to empty values or default values
    $('#address-form input[name="first_name"]').val('');
    $('#address-form input[name="last_name"]').val('');
    $('#address-form input[name="email"]').val('');
    $('#address-form input[name="address_line1"]').val('');
    $('#address-form input[name="address_line2"]').val('');
    $('#address-form input[name="phone"]').val('');
    $('#address-form input[name="city"]').val('');
    $('#address-form input[name="state"]').val('');
    $('#address-form input[name="country"]').val('');
    $('#address-form input[name="postcode"]').val('');

    $('#newAddressModalLabel').text('New Address');

    $('#newAddressModal').modal('show');
});

//

function closeModal() {
    $('#newAddressModal').modal('hide');
}


$(document).on('click', '#del-buton', function(e){
    e.preventDefault()
    var addressId = $(this).closest('.col-lg-6').data('address-id');

    swal({
        title:"Are You Sure",
        text:"Do you want delete this address??",
        icon:"warning",
        buttons: ["Cancel", "Delete"],
        dangerMode: true,
    }).then(function(confirmDelete){
        if (confirmDelete) {
        
            $.ajax({
                method:"GET",
                url:'/delete-address/' + addressId,
                success:function(response){
                    swal({
                        title:"Deleted",
                        text:"Address Deleted!",
                        icon:"success",
                        timer:4000,
                        button:false,
                    }).then(function(){
                        $('#address-block').load(location.href + ' #address-block');
                    });
                }
            })
        }
    });
});

// $(document).ready(function(){
//     $('#form-sub').submit(function(e){
//         e.preventDefault();
//         console.log('formsubmission')
//         var selectedAddress = $('input[name="address_radio"]:checked').val();
//         console.log('selected addresss: ',selectedAddress);
//         var formData = $(this).serialize()
//         console.log('form data : ',formData)
//         formData += '&selected_address='+ selectedAddress;
//         console.log('formdata after updation : ',formData)
//     })
// })


//checkout to payment ---------------------


// $(document).on('submit', '#form-sub', function(e) {
//     e.preventDefault();
//     console.log('formsubmission')
//     var selectedAddress = $('input[name="address_radio"]:checked').val();
//     console.log('selected addresss: ',selectedAddress);
//     var formData = $(this).serialize()
//     console.log('form data : ',formData)
//     formData += '&selected_address='+ selectedAddress;
//     console.log('formdata after updation : ',formData)
//     var url = $(this).attr('action')
//     console.log('url : ',url)

//     $.ajax({
//         method:"POST",
//         url:$(this).attr('action'),
//         data:formData,
//         success:function(response){
//             console.log('response : ',response)
//             if (response.redirect_url){
//                 window.location.href = response.redirect_url;
//             }else {
                
//                 $('.main').append(response.payment_html)
//             }
//         },
//         error:function(xhr, status, error){

//         }
//     })
// });



// function getWeights() {
//     var flavour         = $('#flavorSelect').val();
//     var product_id      = $('#product_id').val();
//     console.log('flavour : ',flavour)
//     console.log('proudct_id : ',product_id)
//     $.ajax({
//         url:'/shop/get-weight/',
//         data:{
//                 'flavour':flavour,
//                 'product_id':product_id,
//         },
//         success:function(response){
//             console.log(response);
//             var weightList = $('#sizeList')
//             console.log('weightlist : ',weightList)
//             console.log('response.weights : ',response.weights)
//             console.log('response.weights.length : ',response.weights.length)
//             weightList.empty();
//             for (var i =0; i<response.weights.length;++i){
//                 var weight =  response.weights[i]
//                 console.log('weight : ',weight)
//                 var listItem = $('<li>').attr('data-flavor',flavour);
//                 console.log('list Item : ',listItem)
//                 var anchor = $('<a>').attr('href', '#').text(weight);
//                 console.log('anchor : ', anchor)
//                 listItem.append(anchor);
//                 weightList.append(listItem)
//             }
//             weightList.on('click', 'li' , function(e){
//                 e.preventDefault()
//                 weightList.find('li').removeClass('active');
//                 $(this).addClass('active');
//                 weight = $(this).text()
                
//                 $.ajax({
//                     url:'/shop/get-product-details/',
//                     data:{
//                         'flavour':flavour,
//                          'weight':weight,
//                          'product_id':product_id,
//                     },
//                     success:function(response) {
//                         console.log(response)
//                     },
                    
//                 })

//                 // weightList.find('li').removeClass('active');
//                 // $(this).addClass('active');
//             });
            

//         },
//     });

// }





function getWeights() {
    var flavour = $('#flavorSelect').val();
    var product_id = $('#product_id').val();
    $('#cart-add-b').css({'display':'none'})
    $('#wishlist-add-b').css({'display':'none'})
    $('#pro-out-stock').css({'display':'none',})

    $.ajax({
        url: '/shop/get-weight/',
        data: {
            'flavour': flavour,
            'product_id': product_id,
        },
        success: function (response) {
            var weightList = $('#sizeList');
            weightList.empty();
            for (var i = 0; i < response.weights.length; ++i) {
                var weight = response.weights[i];
                var listItem = $('<li>').attr('data-flavor', flavour);
                var anchor = $('<a>').attr('href', '#').text(weight);
                listItem.append(anchor);
                weightList.append(listItem);
            }
        },
    });
}

// Event handler for size options
$('#sizeList').on('click', 'li', function (e) {
    e.preventDefault();

    $('#sizeList li').removeClass('active');
    $(this).addClass('active');
    // var flavour = $(this).data('flavor');
    var flavour = $('#flavorSelect').val();
    var weight = $(this).text();
    var product_id = $('#product_id').val();
    // console.log('flavour : ', flavour)
    // console.log('weight : ', weight)
    // console.log('product_id : ', product_id)
    
    if (flavour != null){
        $.ajax({
            url: '/shop/get-product-details/',
            data: {
                'flavour': flavour,
                'weight': weight,
                'product_id': product_id,
            },
            success: function (response) {
                // console.log(response);
                quantity = response.quantity;
                price    = response.price
                // console.log('quantity : ',quantity)
                // console.log('price : ', price)
                $('#price_pro').text(' Price: ₹' + price)
                 if (quantity > 0){
                    $('#cart-add-b').css({'display':'block',})

                    //wisht list
                    $('#wishlist-add-b').css({'display':'block'})

                    $('#pro-out-stock').css({'display':'none',})
                    $('#quantity').text(quantity + ' stocks are available')

                    // assign input values
                    $('#flavour_pro').val(flavour)
                    $('#weight_pro').val(weight)
                 } else {
                    $('#cart-add-b').css({'display':'none'})
                    $('#pro-out-stock').css({'display':'block',})
                    $('#wishlist-add-b').css({'display':'block'})
                    $('#quantity').text('Product out of stock')
                    
                    // assign input values
                    $('#flavour_pro').val(flavour)
                    $('#weight_pro').val(weight)
                 }
            },
        });
    }
});

// Attach change event handler to flavor select
$('#flavorSelect').on('change', getWeights);


// order cancel by user

$(document).on('click', '#user-act', function() {
    console.log('button clicked...')
    var orderproductId = $(this).data('orderproduct-id')
    console.log('orderproduct id : ', orderproductId)
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    console.log('csrf token : ', csrfToken)

    swal({
        title:"Are You Sure",
        text:"Do You Want to Cancel This Ordered Product",
        icon:"warning",
        buttons:['Cancel', 'Yes'],
        dangerMode:true
    }).then(function(confirmYes) {
        
        if (confirmYes) {
            $.ajax({
                method:"POST",
                url:"/orders/order-act/",
                data:{
                    'orderproduct_id':orderproductId,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:"",
                        text:"",
                        icon:"success",
                        timer:4000,
                        button:false,
                    }).then(function(){
                        $('#user-order-det-block').load(location.href + ' #user-order-det-block');
                    })
                },
            })
        }
        
    })

    

    

})


// order return

$(document).on('click', '#user-ord-retrn', function(){
    console.log('return button clickeddd....')
    var orderproductId = $(this).data('orderproduct-id')
    console.log('product id : ', orderproductId)
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()

    swal({
        title:"Are You Sure",
        text:"Do you want to Return this product",
        icon:'warning',
        buttons:['Cancel', 'Yes'],
        dangerMode:true,
    }).then(function(confirmYes) {
        if(confirmYes){
            $.ajax({
                method:"POST",
                url:"/orders/order-return/",
                data:{
                    'orderproduct_id':orderproductId,
                    'csrfmiddlewaretoken':csrfToken,
                },
                success:function(response){
                    swal({
                        title:"Returned",
                        text:response.message,
                        icon:'success',
                        timer:4000,
                        button:false,
                    }).then(function(){
                        $('#user-order-det-block').load(location.href + ' #user-order-det-block')
                    })
                }
            })
        }
    })
})



// cartitem quantity increment
function increment(cartitem_id, cartitem_quantity, cartitem_total_price) {
    
    $.ajax({
        url:"/cart/increment-quantity/" + cartitem_id,
        success:function(response){
            if ('message' in response){
                swal({
                    title:"Sorry",
                    text:response.message,
                    icon:"warning",
                    button:false,
                    timer:4000,
                }).then(function(){
                    $('#cartitem-table').load(location.href + ' #cartitem-table')
                    $('#cartcount-block').load(location.href + ' #cartcount-block')
                })
            }
            document.getElementById(cartitem_id).value = response.qty
            document.getElementById(cartitem_total_price).innerHTML = '₹' + response.updated_price;
            document.getElementById('cart-subtotal').innerHTML = '₹' + response.total_amount;
            document.getElementById('total_amnt').innerHTML = '₹' + response.total_amount;
            $('#decrementbtn' + cartitem_id).attr('disabled', false);

        }
    })
}


//Cart item quantity decrement
function decrement(cartitem_id, cartitem_quantity, cartitem_total_price) {
    $.ajax({
        url:"/cart/decrement-quantity/" + cartitem_id,
        success:function(response){
            
            
            if (response.qty == 1){
                $('#decrementbtn' + cartitem_id).attr('disabled', true)
                
                document.getElementById(cartitem_id).value = response.qty
                document.getElementById(cartitem_total_price).innerHTML = '₹' + response.updated_price
                document.getElementById('cart-subtotal').innerHTML = '₹' + response.total_amount
                document.getElementById('total_amnt').innerHTML = '₹' + response.total_amount

            } else {
                document.getElementById(cartitem_id).value = response.qty
                document.getElementById(cartitem_total_price).innerHTML = '₹' + response.updated_price
                document.getElementById('cart-subtotal').innerHTML = '₹' + response.total_amount
                document.getElementById('total_amnt').innerHTML = '₹' + response.total_amount
            }
        }
    })
}


// Delete cartitem

$(document).on('click', '#removeCartitem', function(e){
    e.preventDefault()
    
    cartItemId = $(this).data('cartitem-id')
    
    swal({
        titel:"Are You Sure",
        text:"Do you want remove this item from cart",
        icon:'warning',
        buttons:['Cancel','Remove'],
        dangerMode:true
    }).then(function(confirmRemove) {
        if(confirmRemove){
            
            $.ajax({
                url:"/cart/remove-cartitem/" + cartItemId,
                success:function(response) {
                    swal({
                        title:"Removed",
                        text:response.message,
                        icon:'success',
                        button:false,
                        timer:4000
                    }).then(function() {
                        $('#cartitem-table').load(location.href + ' #cartitem-table')
                        $('#cartcount-block').load(location.href + ' #cartcount-block')
                    })
                }
            })
        }
    })
})














