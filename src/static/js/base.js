

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






















// $('.add-to-cart-button').click(function(e) {
//     e.preventDefault();
//     var productId = $(this).data('product-id');
//     $.ajax({
//       url: 'add_to_cart',
//       type: 'POST',
//       data: { 'product_id': productId ,
//             'X-CSRFToken': csrftoken,
//         },
//       success: function(response) {
//         if (response.success) {
//             // Update the quantity and total price in the navbar
//             $('.basket-quantity').text(response.basket_quantity);
//             $('.basket-total-price').text(response.basket_total_price);
//             // Update the product list in the navbar
//             var productList = response.product_list;  // Assuming you return the list of products in the response
//             var $minicartProductList = $('.minicart-product-list');
//             $minicartProductList.empty();
//             $.each(productList, function(index, product) {
//               var productHtml = '<li>' +
//                 '<a href="singleproduct" class="minicart-product-image">' +
//                 '<img src="' + product.image_url + '" alt="cart products">' +
//                 '</a>' +
//                 '<div class="minicart-product-details">' +
//                 '<h6><a href="#">' + product.name + '</a></h6>' +
//                 '<span>£' + product.price + ' x ' + product.quantity + '</span>' +
//                 '</div>' +
//                 '<button class="close" title="Remove">' +
//                 '<i class="fa fa-close"></i>' +
//                 '</button>' +
//                 '</li>';
//               $minicartProductList.append(productHtml);
//             });
//           } else {
//             // Handle any error messages returned in the response
//             console.log
        
//       error: function(xhr, status, error) {
//         // Handle any errors that occur during the AJAX request.
//       }
//     });
//   });
  