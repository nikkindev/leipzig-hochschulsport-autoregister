## Leipzig Hochschulsport Autoregister


**Info**

Python script to autoregister for sport courses

**Update**

Final request returns with a 200-OK status code displaying registration failure, instead of a 302-Redirection status code with confirmation URL link as Value for the Key 'Location' in 'Response Headers'

**Modules required:**
- Requests
- BeautifulSoup (bs4)
- sys
- re

**Checklist**
- Personal Info
- URLs check
- Headers check from DevTools in Chrome
- KursID check
- Course price check
- Response saved as r4.txt