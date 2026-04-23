/**
 * TikTok Creative Center (TCC) Top Products Exporter
 *
 * Instructions:
 * 1. Go to https://ads.tiktok.com/business/creativecenter/inspiration/top-products/pc/en?region=ID
 * 2. Scroll down to load more products if needed.
 * 3. Open Browser Console (F12 -> Console).
 * 4. Paste this script and press Enter.
 * 5. A 'tcc_products.csv' file will be downloaded.
 */

(function () {
  console.log("Starting TCC Export...");

  const products = [];
  // Select the table rows (TCC uses specific class names)
  const rows = document.querySelectorAll('tr[class*="table-row"]');

  if (rows.length === 0) {
    console.error(
      "No product rows found. Make sure you are on the Top Products page and products are loaded.",
    );
    return;
  }

  rows.forEach((row, index) => {
    try {
      const cells = row.querySelectorAll("td");
      if (cells.length < 3) return;

      // Product Name is usually in a div with specific styling
      const nameEl =
        row.querySelector('span[class*="product-name"]') ||
        row.querySelector('div[class*="product-name"]');
      const name = nameEl ? nameEl.innerText.trim() : "Unknown Product";

      // Popularity/Performance
      const performance = cells[2] ? cells[2].innerText.trim() : "0";

      // Category
      const category = cells[1] ? cells[1].innerText.trim() : "Unknown";

      products.push({
        "Product Name": name,
        Category: category,
        Performance: performance,
        Source: "TikTok Creative Center",
      });
    } catch (e) {
      console.error("Error parsing row " + index, e);
    }
  });

  if (products.length === 0) {
    console.error("No data extracted.");
    return;
  }

  // Convert to CSV
  const headers = Object.keys(products[0]).join(",");
  const csvContent = [
    headers,
    ...products.map((p) =>
      Object.values(p)
        .map((v) => `"${v}"`)
        .join(","),
    ),
  ].join("\n");

  // Download File
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  const url = URL.createObjectURL(blob);
  link.setAttribute("href", url);
  link.setAttribute(
    "download",
    `tcc_products_${new Date().toISOString().split("T")[0]}.csv`,
  );
  link.style.visibility = "hidden";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  console.log(`Exported ${products.length} products successfully!`);
})();
