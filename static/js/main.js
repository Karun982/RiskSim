document.getElementById("simForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const amount = document.getElementById("amount").value;
  const years = document.getElementById("years").value;
  const asset = document.getElementById("asset").value;

  fetch('/simulate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      amount: Number(amount),
      years: Number(years),
      asset_type: asset
    })
  })
  .then(res => res.json())
  .then(data => {
    console.log(data);

    // Store data for next page
    localStorage.setItem("resultData", JSON.stringify(data));

    // Redirect
    window.location.href = "/result";
  })
  .catch(err => console.error(err));
});