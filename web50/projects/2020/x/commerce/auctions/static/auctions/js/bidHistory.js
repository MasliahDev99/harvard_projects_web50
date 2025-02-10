document.addEventListener('DOMContentLoaded', function() {
    function updateAuctionState() {
        const now = new Date();
        const bidRows = document.querySelectorAll('tr[data-bid-id]');
        console.log(`Updating ${bidRows.length} bids`);

        bidRows.forEach(row => {
            const bidId = row.dataset.bidId;
            const auctionId = row.dataset.auctionId;
            const userId = document.body.dataset.userId;
            console.log(`Processing bid ${bidId} for auction ${auctionId}, user ${userId}`);

            fetch(`/api/auctions/${auctionId}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(auction => {
                console.log('Auction data:', auction);
                const auctionEndDate = new Date(`${auction.end_date}T${auction.end_time}`);
                console.log(`Auction end date: ${auctionEndDate}, Current time: ${now}`);

                if (auctionEndDate < now) {
                    const statusCell = row.querySelector('.bid-status');
                    const currentStatus = statusCell.textContent.trim().toLowerCase();
                    console.log(`Current status: ${currentStatus}`);

                    if (currentStatus === 'in process') {
                        const isWinner = auction.winner && auction.winner.id === parseInt(userId);
                        console.log(`Is winner: ${isWinner}`);

                        fetch(`/api/bids/${bidId}/`, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                            body: JSON.stringify({
                                status: isWinner ? 'Winner' : 'Lost'
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Bid update response:', data);
                            statusCell.textContent = isWinner ? 'Winner' : 'Lost';
                            statusCell.className = `bid-status badge ${isWinner ? 'bg-success' : 'bg-danger'}`;
                        })
                        .catch(error => console.error('Error updating bid:', error));
                    }
                }
            })
            .catch(error => console.error('Error fetching auction:', error));
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    updateAuctionState();
    setInterval(updateAuctionState, 5000);
});