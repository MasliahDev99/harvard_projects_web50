document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Attach send_email function to the form submission
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  show_view('compose-view');
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  show_view('emails-view');
  document.querySelector('#mailbox-title').innerHTML = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);
  
  fetch(`/emails/${mailbox}`)
      .then(response => response.json())
      .then(emails => {
          const emailList = document.querySelector('#email-list');
          emailList.innerHTML = '';
          emails.forEach(email => {
              const emailElement = create_email_element(email, mailbox);
              emailList.appendChild(emailElement);
          });
      })
      .catch(error => console.error('Error:', error));
}

function create_email_element(email, mailbox) {
  const element = document.createElement('a');
  element.classList.add('list-group-item', 'list-group-item-action', 'd-flex', 'justify-content-between', 'align-items-center');
  element.href = '#';
  element.innerHTML = `
      <div>
          <strong>${mailbox === 'sent' ? email.recipients.join(', ') : email.sender}</strong>
          <span class="ml-2">${email.subject}</span>
      </div>
      <span class="text-muted">${email.timestamp}</span>
  `;
  
  // Cambiamos el color de fondo según si el correo ha sido leído o no
  element.classList.add(email.read ? 'bg-light' : 'bg-white');
  
  element.addEventListener('click', () => view_email(email.id, mailbox));
  return element;
}

function view_email(email_id, mailbox) {
  show_view('email-view');
  fetch(`/emails/${email_id}`)
      .then(response => response.json())
      .then(email => {
          document.querySelector('#email-content').innerHTML = `
              <h4>${email.subject}</h4>
              <p><strong>From:</strong> ${email.sender}</p>
              <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
              <p><strong>Timestamp:</strong> ${email.timestamp}</p>
              <hr>
              <p>${email.body}</p>
          `;
          
          const actionsDiv = document.querySelector('#email-actions');
          actionsDiv.innerHTML = '';
          
          if (mailbox !== 'sent') {
              const archiveBtn = document.createElement('button');
              archiveBtn.textContent = email.archived ? 'Unarchive' : 'Archive';
              archiveBtn.className = `btn ${email.archived ? 'btn-secondary' : 'btn-primary'} mr-2`;
              archiveBtn.addEventListener('click', () => archive_email(email_id, !email.archived));
              actionsDiv.appendChild(archiveBtn);
          }
          
          const replyBtn = document.createElement('button');
          replyBtn.textContent = 'Reply';
          replyBtn.className = 'btn btn-info';
          replyBtn.addEventListener('click', () => reply_to_email(email));
          actionsDiv.appendChild(replyBtn);

          if (!email.read) {
              mark_as_read(email_id);
          }
      })
      .catch(error => console.error('Error:', error));
}

function archive_email(email_id, archive_status) {
  fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({ archived: archive_status })
  })
  .then(() => load_mailbox(archive_status ? 'archive' : 'inbox'))
  .catch(error => console.error('Error:', error));
}

function mark_as_read(email_id) {
  fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({ read: true })
  })
  .catch(error => console.error('Error:', error));
}

function reply_to_email(email) {
  compose_email();
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = email.subject.startsWith('Re: ') ? email.subject : `Re: ${email.subject}`;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n\n${email.body}\n\n`;
}

function send_email(event) {
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({ recipients, subject, body })
  })
  .then(response => response.json())
  .then(result => {
      if (result.error) {
          show_error(result.error);
      } else {
          load_mailbox('sent');
      }
  })
  .catch(error => console.error('Error:', error));
}

function show_view(view_id) {
  document.querySelectorAll('#emails-view, #email-view, #compose-view').forEach(view => {
      view.classList.add('d-none');
  });
  document.querySelector(`#${view_id}`).classList.remove('d-none');
}

function show_error(message) {
  const errorDiv = document.querySelector('#compose-error');
  errorDiv.textContent = message;
  errorDiv.classList.remove('d-none');
}