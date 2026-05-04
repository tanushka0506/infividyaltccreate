@app.route('/')
def home():
    return """
    <h2>Employee Activity Dashboard</h2>
    <div id="data"></div>

    <script>
    async function load() {
        let res = await fetch('/data?nocache=' + new Date().getTime());
        let data = await res.json();

        let html = "";

        data.forEach(item => {
            let localTime = new Date(item.timestamp).toLocaleString('en-IN');

            html += `<div style="border:1px solid #ccc; padding:10px; margin:5px;">
                <b>${item.user}</b><br>
                Site: ${item.domain}<br>
                Time: ${localTime}
            </div>`;
        });

        document.getElementById("data").innerHTML = html;
    }

    setInterval(load, 3000);
    load();
    </script>
    """
