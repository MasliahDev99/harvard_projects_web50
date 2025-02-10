document.addEventListener('DOMContentLoaded', function() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            const descriptions = this.querySelectorAll('.collapse');
            descriptions.forEach(description => {
                description.classList.remove('show');
            });
        });
    });

    function updateCountdown() {
        const now = new Date();
        const auctionCards = document.querySelectorAll('.card[data-auction-id]');

        auctionCards.forEach(card => {
            const auctionId = card.dataset.auctionId;
            const endDate = new Date(`${card.dataset.endDate}T${card.dataset.endTime}`);
            const timeRemaining = endDate - now;

            const countdownElement = card.querySelector('.auction-countdown');
            const endTimeElement = card.querySelector('.auction-end-time');

            if (timeRemaining > 0) {
                const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
                const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

                if (timeRemaining < 24 * 60 * 60 * 1000) {
                    countdownElement.textContent = `Ends in: ${hours}h ${minutes}m ${seconds}s`;
                    countdownElement.classList.remove('d-none');
                    endTimeElement.classList.add('d-none');
                } else {
                    countdownElement.classList.add('d-none');
                    endTimeElement.classList.remove('d-none');
                }
            } else {
                countdownElement.textContent = 'Auction ended';
                countdownElement.classList.remove('d-none');
                endTimeElement.classList.add('d-none');
                endTimeElement.style.textDecoration = 'line-through';
                endTimeElement.style.color = 'red';

                let reloadFlag = sessionStorage.getItem('auction_' + auctionId + '_reloaded');
                if (!card.classList.contains('auction-ended') && !reloadFlag) {
                    card.classList.add('auction-ended');
                    sessionStorage.setItem('auction_' + auctionId + '_reloaded', true);
                    window.location.reload();
                }

                // Fetch auction details to check for a winner
                fetch(`/api/auctions/${auctionId}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(auction =>{
                    if (auction.winner) {
                        const winnerElement = card.querySelector('.auction-winner');
                        winnerElement.textContent = `Winner: ${auction.winner}`;
                        winnerElement.classList.remove('d-none');
                    }
                })

            }   
        });
    }

    // Update countdown every second
    setInterval(updateCountdown, 1000);

    // Initial update
    updateCountdown();
});