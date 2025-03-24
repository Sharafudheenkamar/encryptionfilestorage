
$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
    $('#dismiss, .overlay').on('click', function () {
        $('#sidebar').removeClass('active');
    });
});

// // JavaScript to set the complaint ID in the modal title when a "Reply" button is clicked
// document.querySelectorAll('.reply-btn').forEach(button => {
//     button.addEventListener('click', function () {
//         const complaintId = this.getAttribute('data-complaint-id');
//         document.querySelector('.modal-title-id').textContent = complaintId;
//     });
// });

// // JavaScript to handle form submission
// document.getElementById('replyForm').addEventListener('submit', function (event) {
//     // Prevent the default form submission
//     event.preventDefault();


//     // Display success message
//     alert('file renamed successfully!');

//     // Close the modal
//     $('#replyModal').modal('hide');
// });

// function downloadFile(fileId) {
//     // const fileUrl = `/download-file/${fileId}`; // Replace with your actual file URL
//     const fileUrl = `logo.png`;
//     const link = document.createElement('a');
//     link.href = fileUrl;
//     link.setAttribute('download', '');  
//     link.click();
// }
 const starContainer = document.getElementById('star-rating');
  const maxStars = 5;

  // Generate stars dynamically
  for (let i = 1; i <= maxStars; i++) {
    const star = document.createElement('i');
    star.classList.add('fa', 'fa-star');
    star.dataset.rating = i;  // Store rating value
    starContainer.appendChild(star);

    // Add click event
    star.addEventListener('click', () => {
      updateStars(i);
    });
  }

  // Update stars based on selected rating
  function updateStars(rating) {
    const stars = starContainer.querySelectorAll('.fa-star');
    stars.forEach(star => {
      star.classList.toggle('checked', star.dataset.rating <= rating);
    });
  }

  // Initialize with default rating from data attribute
  const initialRating = parseInt(starContainer.dataset.rating, 10);
  updateStars(initialRating);

  