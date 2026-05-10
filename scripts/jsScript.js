const pass = Uint8Array.from([0x12]);
const name = Uint8Array.from([0x12]);

function encodeField(key, valueBytes) {
  return `${key}=` + Array.from(valueBytes)
    .map(b => `%${b.toString(16).padStart(2, '0').toUpperCase()}`)
    .join('');
}

const body = encodeField("user", name) + "&" +
             encodeField("password", pass) + "&" +
             "csrf=00000d683338f7c146d91828dd4cae3ec5a4854b1c78ed4261d4f1d4347c930cba1649&";

fetch("/login", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body
})
.then(res => res.text())
.then(console.log)
.catch(console.error);