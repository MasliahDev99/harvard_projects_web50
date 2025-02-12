document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Attach send_email function to the form submission
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // Open email
  document.querySelector('#emails-view').addEventListener('click', function(event) {
    const emailElement = event.target.closest('.email'); 
    if (emailElement) {
      const emailID = emailElement.getAttribute('data-email-id');
      view_email(emailID);
    }
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

function mark_as_read(emailID,emailDiv){
    fetch(`/emails/${emailID}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
    .then(() => {
      // Change background color to gray
      emailDiv.style.backgroundColor = 'gray';
      console.log(`Email ${emailID} clicked and marked as read!`);
    });
}

function render_email(email){
    const emailDiv = document.createElement('div');
    emailDiv.className = 'email list-group-item mb-2';
    emailDiv.setAttribute('data-email-id', email.id);
    emailDiv.innerHTML = `
      <div class="d-flex justify-content-between">
          <div>
            <strong>From: ${email.sender}</strong>
            <p>${email.timestamp}</p>
          </div>
      </div>
        <strong>Subject: ${email.subject}</strong>
    `;
    emailDiv.style.backgroundColor = email.read ? '#d3d3d3' : 'white';
    
    emailDiv.addEventListener('click', function() {
      mark_as_read(email.id, emailDiv);
    });

    document.querySelector('#emails-view').append(emailDiv);
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none'; 
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${capitalize(mailbox)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Clear the emails view
        document.querySelector('#emails-view').innerHTML = `<h3>${capitalize(mailbox)}</h3>`;

        // render each email
        emails.forEach(email => render_email(email));
        
    })
    .catch(error =>{console.error('Error fetching emails: ',error);
    });
}


function send_email(event){
  event.preventDefault();

  // Get the values from the form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body,
      })
    })
    .then(response => response.json())
    .then(result => {
        handle_email_response(result, () => load_mailbox('sent'), '#compose-error');
    })
    .catch(error =>{
      console.error('Error: ',error);
    });
}

function handle_email_response(result, onSuccess, errorElementSelector){
  /* 
    Handles the response from an email-related server request.

    This function is designed to be flexible and reusable across different parts of the application.
    It proccesses the server response, checking for errors and executing a callback function on success
    if provided.

    Parameters:
    @param {Object} result - The response from the server.
    @param {Function} onSuccess - A callback function to be executed on success.
    @param {string} errorElementSelector - The selector for the element to display error messages.

    The flexibility of this function comes from its ability to handle different types of responses and execute context-specific actions through the onSuccess callback.
    By centralizing response handling, the code becomes more modular and easier to maintain.
  
  */
  if(result.error){
    document.querySelector(errorElementSelector).textContent = result.error;
    console.error("Error: ",error);
  }else{
    console.log("Email sent: ", result);
    if (onSuccess) onSuccess();
  }
}



//  view email
function view_email(email_id){
  // Show the email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Fetch the email
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Display the email details
    document.querySelector('#email-view').innerHTML = `
      <h3>${email.subject}</h3>
      <p><strong>From:</strong> ${email.sender}</p>
      <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
      <p><strong>Timestamp:</strong> ${email.timestamp}</p>
      <hr>
      <p>${email.body}</p>
    `;

    // Mark the email as read
    if (!email.read) {
      mark_as_read(email_id, null);
    }

    // Add Archive button
    const archiveBtn = document.createElement('button');
    archiveBtn.textContent = email.archived ? 'Unarchive' : 'Archive';
    archiveBtn.className = 'btn ' + (email.archived ? 'btn-success' : 'btn-danger');
    archiveBtn.style.marginRight = '10px';
    archiveBtn.addEventListener('click', () => {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then(() => {
        // Reload the inbox or archive mailbox after archiving/unarchiving
        load_mailbox('inbox');
      });
    });

    document.querySelector('#email-view').append(archiveBtn);

    // Add reply button
    const replyBtn = document.createElement('button');
    replyBtn.textContent = 'reply';
    replyBtn.className = 'btn btn-primary';
    replyBtn.addEventListener('click', () => {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;

  
    });



    document.querySelector('#email-view').append(replyBtn);
    


  })
  .catch(error => console.error('Error fetching email:', error));
}