

$(document).ready(function() {
    // Add to Cart button click event
    $('.add-to-cart-button').on('click', function(e) {
        e.preventDefault();
        
        // Retrieve the product ID
        const productID = $(this).data('product-id');
        const productQuantity = $('#product-quantity').val();
        console.log(productID)
        
        $.ajax({
            type: 'POST',
            url: productID + "/add_to_cart/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
                quantity: productQuantity
            },
            success: function(response) {
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
                    alert(response.message);
                } else {
                    alert('Failed to add the product to the cart.');
                }
            },
            error: function(xhr, status, error) {
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

        
        $.ajax({
            type: 'POST',
            url: productID + "/remove_from_cart/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
            },
            success: function(response) {
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
                    alert(response.message);
                } else {
                    alert('Failed to delete the product from the cart.');
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});



$(document).ready(function() {
    // Add to Cart button click event
    $('.add-to-wishlist-button').click(function(e) {
        e.preventDefault();

        // Retrieve the product ID
        const productID = $(this).data('product-id');
        console.log(productID)
        
        $.ajax({
            type: 'POST',
            url: productID + "/add_to_wishlist/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
            },
            success: function(response) {
                if (response.success) {
                    $('#wishlist-quantity').text(response.wishlist_quantity);

                    alert(response.message);
                } else {
                    // Show error message
                    alert('Failed to add the product to the wishlist.');
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});





$(document).ready(function() {
    $('.remove-from-wishlist-button').click(function(e) {
        e.preventDefault();
        console.log("wishlist+++++++++++++++++++++++++++++")

        const productID = $(this).data('product-id');
        console.log(productID)
        
        $.ajax({
            type: 'POST',
            url: productID + "/remove_from_wishlist/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
            },
            success: function(response) {
                if (response.success) {
                    // Update the wishlist information in navbar
                    $('#wishlist-quantity').text(response.wishlist_quantity);

                    $(e.target).closest('tr').remove();

                    alert(response.message);
                } else {
                    // Error message
                    alert('Failed to add the product to the wishlist.');
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});


  
$(document).ready(function() {
    $('.subscribe-btn').click(function(e) {
        e.preventDefault();

        const subscribeForm = document.getElementById('subscribe-form');
        const emailInput = document.getElementById('mc-email').value;
        
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
                    alert('Subscription successful!');
                } else {
                    alert('Subscription failed. ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});








// Assuming you have a product list container with id "product-list"
$.ajax({
    type: 'POST',
    url: '/search/',  // Update with your search page URL
    data: {
      category: selectedCategoryId,       // Retrieve the selected category ID
      subcategory: selectedSubcategoryId, // Retrieve the selected subcategory ID
      color: selectedColor                 // Retrieve the selected color
    },
    success: function(response) {
      var productContainer = $('#product-list');
      productContainer.empty(); // Clear existing products
  
      if (response.products.length > 0) {
        // Iterate over the filtered products and add them to the product container
        $.each(response.products, function(index, product) {
          var productHtml = '<div class="product">' +
            '<h3>' + product.name + '</h3>' +
            '<p>' + product.description + '</p>' +
            '</div>';
          productContainer.append(productHtml);
        });
      } else {
        // Display a message if no products are found
        productContainer.append('<p>No products found.</p>');
      }
    },
    error: function(xhr, status, error) {
      // Handle the error if needed
      console.log(error);
    }
  });
  