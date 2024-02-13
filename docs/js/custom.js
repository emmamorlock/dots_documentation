document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.card-body').forEach(function (body) {
        body.style.display = 'none';
    });
    document.querySelectorAll('.collapse-card').forEach(function (collapse) {
        fetchDataForCollapse(collapse);
    });
});


function toggleCollapse(headerElement) {
    const cardBody = headerElement.nextElementSibling;
    const chevron = headerElement.querySelector('.chevron');
    if (cardBody.style.display === "none" || cardBody.style.display === '') {
        cardBody.style.display = "block";
        chevron.classList.add('rotated');
    } else {
        cardBody.style.display = "none";
        chevron.classList.remove('rotated');
    }
}

function fetchDataForCollapse(collapse) {
    const url = collapse.getAttribute('data-url');
    const cardBody = collapse.querySelector('.card-body');
    if (url) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                cardBody.innerHTML = `<pre><code class="json">${JSON.stringify(data, null, 2)}</code></pre>`;
                hljs.highlightBlock(cardBody.firstChild, {language: 'json'});
                hljs.highlightAll();
            })
            .catch(error => {
                cardBody.innerHTML = `<p>Failed to fetch data, retry later.</p>`;
            });
    }
}



