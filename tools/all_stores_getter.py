import requests

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en',
    'Business-User-Agent': 'PCXWEB',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': 'lcl_lang_pref=en; jjSPnsABk=A0D8jeqNAQAA4yvp6WbRAMp_I9FEHMVP6pvpS2lusCTtK9uviuv-VZ45FMkSAZlcKPeuclIDwH8AAEB3AAAAAA|1|0|e040beb116765356be05073aef087a52a7516061; Origin_Session_Cookie=B; PIM-SESSION-ID=JX3FQHpz5aU3zIu9; kameleoonVisitorCode=ky3etx96s34d442j; Max-Age=31536000; Path=/; Domain=https://www.loblaws.ca; customer_state=anonymous; last_selected_store=1050; _spvid_ses.5f05=*; bm_sz=FF04528D9E7BE354F914CD4D73656903~YAAQKpYqF6HgLR2PAQAARecOIhc9cgLFSYrkEoQa3prnHvryKQPImowUZCFVt/+g09XW6klb1zzOxRs9JW3sWAaZ5+KVZXCJmQSwWbSNKElMWn6fllzfyJTzmJRL78oumR9sr8Ycj0H/z+OWEyl4IBqbtmIuGn5taAqwBTI7eZYakVyiy3SaQA0tR7HabYCSZDrZQCmuaq3ZVfD+Wj7mHt+Y4bTTCoZshrDC3fSLNXuLAakVTgkvLd+DRD5+bNtn+NHNrT0w8lk66x5pob5kAvxbgqpLV9ULxUGKycJpgNq9M8d1a6707jPFsmuBSP+jykTUJgCR/SNFPakumCQFLo7BB11ecsQVJW5VtR6Q3Z/ffuvY0Bo1pW0BUrufvlmns8yvoCLzZVP8i4431PPD6pYjSpp8lQKUJNgafnfMeY3hLEWR/uEnYamEIKBiQEueUk2H21bfhr6gD14VeyI5O8eFrp6AshpoSN2gJhzz4k5j1YQatKZPelif247mIgXLJeyUazvcbXOQBav827XzPADbnXNr85PqVl3zrTP7KXVK0IXt2M8/sD1X1BMgiwAB48KT87fV7g9DhQ==~3617860~3355952; bm_mi=A5EBA6EF5E258618A2DD2E7F2D27AE39~YAAQLpYqF02Kju6OAQAA9UsQIhc0bcj+E++/Ea7HqJEITHe34jolRIK4sug0UzAaLiSAmDjy+LarFrPJ2X80lg/pnJcN2aPlKaHvkmi5ZxKNpEc+7kJanVmlGhmNbgZyjczoUhJO/3EMpxakFvJPrcq+S6pv5XoGS9iZ4wI5wboAKBWI1E9iAONzIXBbU/PXIGXkgHtjD/ZFu/0bBJo5uXiA9ssjXbdDIaAcstQRmwWmTGigNOF1QIxqw5xrsrAmFSbDhkpbVx7VgNq+WdX8cY+hDiBUdgsr8Yky2MT9DPZ6bYMpHGgM+BkWWa3addNbRzosy9EMBFO5x2dmtTyASyR1OKBf3u4=~1; bm_sv=ADA65C7CFDCCB14A19CBDE44B9028D37~YAAQLpYqF6qpju6OAQAASYMQIheCU7JMY4kce8iSe1LJsLJnCgfIHD/fU1+EeikSFTVjlofoZ9mS6y+aObArdMiONWtHTCEbykPRUpqnpQybquBi30XHgRkBteyF5BdsjePNlM+nk0kBtsR0QqAnLDQJeAy+Ymw2kmqlDHH8xLrj9VD1rse24qN90hjDA4YOtjxpXBRyoByWF+dFHA43+pp5wn1l78y7D2E/cLNHazalltcsVM1rSTQMLugTmb1/lA==~1; ak_bmsc=52175A10B579A655E348DBD3BAFCD2AD~000000000000000000000000000000~YAAQJ5YqF/ghAyGPAQAAXowQIhfUzxHGTTxjXvd2ggbP0frzy/JMuyPVZOycqiNPrkDmRwRF1WNovJqvqnUr4MMntbjeCLGh9EZUqqnv6/n+djGN3O2ScRFFSJaJlhY74dmQaVOEzPAJQbzZi91l3YPXsMd+/oGiWEx6ZMLqLDlRCqHhkUSzx4jwzXWaiQFZBGIvVTaFhZd5kJfgcMnYilQUeZDo9SXkaY/niMi5FrIU7vdZzwQ4U50L0GQd3noXqEELF5rWAA04l2yR0ks80LL7zF/I1OjpOpubnVpzDcR8w2o8IbPpW6R02WvADYh4uVFfdjJ0e2nrnU2LpSco7tMmMHtKuO4kPxa9gAhqL8b8B5F1Hy2cveLAsE6k7X9YCTQH+5HHgdianOdA4LsR6dtC/GfoB4OkcvqkIzjwgHrSylqtXWNPUFSD2HF5/lQcnw==; SameSite=None; lastVisited=1714263761752; CoQWDnyf=lZbYZ3Hh; akavpau_vp=1714264064~id=c00cca008456171267005297d8f0b200; ADRUM_BTa=R:47|g:582c22ee-6b53-4142-a2d7-674e88c588e7|n:lblw_afe7f4d6-4637-4e11-95bb-0a169ff97498; ADRUM_BT1=R:47|i:352462|e:110|d:2; _abck=6D3684E4EE9E998E1848EC87ECDC5080~0~YAAQRQp8aIULExGPAQAArTMVIgtlOtVMVhqiYhFwxJvEchluKCCJLLqzdpaCh6O9MyuMH/G8hZGfqda4G5OR+WiT8tMe4sxaqRBkLP1oWZgBZSWgayOB9xHP20+AxRwM1G1sfuOQve9FsMOhN0zijIUvwCY623CL9ND6rICBhRUhXrKfrc0I4/k6G5qFxWauDOin9hBhufR4sLHzq63LoNQ145y5T0pllxpV++9S6mqOdLXAUNaTjPsxyZ+VNuSjPbdstf46CqD2GdbYcedYlGyjauoAuUIsCuipm9qHAqzTyupfB8SkPIhQk49rFpxHl431qWBfPesyypUMEPkgo2k7YzuJnR62ZJZUMAU3WRT6O1IOl7TxQNy3jsGjaA==~-1~-1~1714266954; _spvid_id.5f05=3c9bfa55-a832-41bd-971b-2425eec551ef.1709037194.17.1714263766.1714253061.e33ae1d1-5151-444e-9406-3847fb8db6f3.a800214a-c182-4b4f-9140-305702aa4771.8cd3190b-5407-4b04-aeb6-376478187366.1714263231312.36',
    'Pragma': 'no-cache',
    'Referer': 'https://www.loblaws.ca/store-locator?type=store',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Site-Banner': 'loblaw',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def get_all_stores():
    r = requests.get('https://www.loblaws.ca/api/pickup-locations', headers=HEADERS)
    return r.json()