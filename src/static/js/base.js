

$(document).ready(function() {
    // Add to Cart button click event
    $('.add-to-cart-button').on('click', function(e) {
        e.preventDefault();
        
        // Retrieve the product ID
        const productID = $(this).data('product-id');
        const productQuantity = $('#product-quantity').val();
        // const prodID = $('#product-id').val();
        console.log(productID)
        
        // Send AJAX request to add the product to the cart
        $.ajax({
            type: 'POST',
            url: productID + "/add_to_cart/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
                quantity: productQuantity
            },
            success: function(response) {
                // Handle the response
                if (response.success) {
                    // Update the basket information in the navbar
                    $('#basket-quantity').text(response.basket_quantity);
                    $('#basket-total-price').text('£' + response.basket_total_price);
                    $('#basket-total-price2').text('£' + response.basket_total_price);
                    
                    // Update the product list in the navbar
                    var productList = response.product_list;
                    var $minicartProductList = $('.minicart-product-list');
                    $minicartProductList.empty();
                    productList.forEach(function(product) {
                        var productHtml = '<li>' +
                            '<a href=" ' + product.url + ' " class="minicart-product-image">' +
                            '<img src="' + product.picture + '" alt="cart products">' +
                            '</a>' +
                            '<div class="minicart-product-details">' +
                            '<h6><a href="'+ product.url +'">' + product.name + '</a></h6>' +
                            '<span>£' + product.unit_price + ' x ' + product.quantity + '</span>' +
                            '</div>' +
                            '<button class="close remove-from-cart-button" data-product-id="' + product.id + '" title="Remove">' +
                            '<i class="fa fa-close"></i>' +
                            '</button>' +
                            '</li>';
                        $minicartProductList.append(productHtml);
                    });
                    // Show a success message (optional)
                    alert(response.message);
                } else {
                    // Show an error message (optional)
                    alert('Failed to add the product to the cart.');
                }
            },
            error: function(xhr, status, error) {
                // Handle the error (optional)
                console.log(error);
            }
        });
    });
});





$(document).ready(function() {
    // Add to Cart button click event
    $('.minicart-product-list').on('click', '.remove-from-cart-button', function(e) {
        e.preventDefault();
        console.log("asdfghjklkjhgfdsasdfghj")

        // Retrieve the product ID
        const productID = $(this).data('product-id');
        console.log(productID)
        // const prodID = $('#product-id').val();
        
        // Send AJAX request to add the product to the cart
        $.ajax({
            type: 'POST',
            url: productID + "/remove_from_cart/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
            },
            success: function(response) {
                // Handle the response
                if (response.success) {
                    // Update the basket information in the navbar
                    // console.log(response.basket_quantity)
                    $('#basket-quantity').text(response.basket_quantity);
                    $('#basket-total-price').text('£' + response.basket_total_price);
                    $('#basket-total-price2').text('£' + response.basket_total_price);
                    
                    // Update the product list in the navbar
                    var productList = response.product_list;
                    var $minicartProductList = $('.minicart-product-list');
                    $minicartProductList.empty();
                    productList.forEach(function(product) {
                        var productHtml = '<li>' +
                            '<a href=" ' + product.url + ' " class="minicart-product-image">' +
                            '<img src="' + product.picture + '" alt="cart products">' +
                            '</a>' +
                            '<div class="minicart-product-details">' +
                            '<h6><a href="'+ product.url +'">' + product.name + '</a></h6>' +
                            '<span>£' + product.unit_price + ' x ' + product.quantity + '</span>' +
                            '</div>' +
                            '<button class="close remove-from-cart-button" data-product-id="' + product.id + '" title="Remove">' +
                            '<i class="fa fa-close"></i>' +
                            '</button>' +
                            '</li>';
                        $minicartProductList.append(productHtml);
                    });
                    // Show a success message (optional)
                    alert(response.message);
                } else {
                    // Show an error message (optional)
                    alert('Failed to delete the product from the cart.');
                }
            },
            error: function(xhr, status, error) {
                // Handle the error (optional)
                console.log(error);
            }
        });
    });
});



$(document).ready(function() {
    // Add to Cart button click event
    // $('.hm-wishlist').on('click', '.add-to-wishlist-button', function(e) 
    $('.add-to-wishlist-button').click(function(e) {
        e.preventDefault();
        console.log("wishlist+++++++++++++++++++++++++++++")

        // Retrieve the product ID
        const productID = $(this).data('product-id');
        console.log(productID)
        
        // Send AJAX request to add the product to the wishlist
        $.ajax({
            type: 'POST',
            url: productID + "/add_to_wishlist/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
            },
            success: function(response) {
                // Handle the response
                if (response.success) {
                    // Update the wishlist information in the navbar
                    $('#wishlist-quantity').text(response.wishlist_quantity);

                    alert(response.message);
                } else {
                    // Show an error message (optional)
                    alert('Failed to add the product to the wishlist.');
                }
            },
            error: function(xhr, status, error) {
                // Handle the error (optional)
                console.log(error);
            }
        });
    });
});





$(document).ready(function() {
    // Add to Cart button click event
    // $('.hm-wishlist').on('click', '.add-to-wishlist-button', function(e) 
    $('.remove-from-wishlist-button').click(function(e) {
        e.preventDefault();
        console.log("wishlist+++++++++++++++++++++++++++++")

        // Retrieve the product ID
        const productID = $(this).data('product-id');
        console.log(productID)
        
        // Send AJAX request to add the product to the wishlist
        $.ajax({
            type: 'POST',
            url: productID + "/remove_from_wishlist/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
            },
            success: function(response) {
                // Handle the response
                if (response.success) {
                    // Update the wishlist information in the navbar
                    $('#wishlist-quantity').text(response.wishlist_quantity);

                    $(e.target).closest('tr').remove();

                    alert(response.message);
                } else {
                    // Show an error message (optional)
                    alert('Failed to add the product to the wishlist.');
                }
            },
            error: function(xhr, status, error) {
                // Handle the error (optional)
                console.log(error);
            }
        });
    });
});



  
//   // Handle form submission via AJAX
//   const subscribeForm = document.getElementById('subscribe-form');
//   console.log("wishlist+++++++++++++++++++++++++++++")
//   const csrfToken = getCookie('csrftoken');

//   subscribeForm.addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent form submission

//     const emailInput = document.getElementById('mc-email').value;

//     // Send AJAX request to subscribe
//       $.ajax({
//         type: 'POST',
//         url:"/subscribe/",
//         data: {
//             csrfmiddlewaretoken: csrftoken,
//             emailInput: emailInput,
//         },
//     })
//       .then(response => response.json())
//       .then(data => {
//         if (data.success) {
//           // Subscription successful, handle success message or update UI
//           alert('Subscription successful!');
//           subscribeForm.reset();
//         } else {
//           // Subscription failed, handle error message or update UI
//           alert('Subscription failed. Please try again.');
//         }
//       })
//       .catch(error => {
//         // Handle error
//         console.error(error);
//         alert('An error occurred. Please try again later.');
//       });
//   });



  
$(document).ready(function() {
    $('.subscribe-btn').click(function(e) {
        e.preventDefault();
        console.log("btn btn btn+++++++++++++++++++++++++++++")

        // Retrieve the product ID
        const subscribeForm = document.getElementById('subscribe-form');
        const emailInput = document.getElementById('mc-email').value;
        
        // Send AJAX request to add the product to the wishlist
        $.ajax({
            type: 'POST',
            url:"/subscribe/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                emailInput: emailInput,
            },
            success: function(response) {
                // Handle the response
                if (response.success) {
                    // Update the wishlist information in the navbar
                    alert('Subscription successful!');

                } else {
                    // Show an error message (optional)
                    alert('Subscription failed. Please try again.');
                }
            },
            error: function(xhr, status, error) {
                // Handle the error (optional)
                console.log(error);
            }
        });
    });
});


