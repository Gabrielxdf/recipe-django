(async function() {
    console.clear();
    const headers = {
        // authorization: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ4NzMyNzQ1LCJpYXQiOjE2NDg3MjkxNDUsImp0aSI6IjJiNDJhNGM2MDJmMjQ1ZjQ4ZTNlMjNjZTkyYWI1ZDdjIiwidXNlcl9pZCI6MTF9.I_D3Dw2CsHknxVSlYR1NK5EmIDu6EHoZKLkslUg_CtM'
    };
    const config = {
        method: 'GET',
        headers: headers,
    };
    const response = await fetch(
        'http://127.0.0.1:8000/authors/api/me/',
        config
    );
    
    const json = await response.json();

    console.log('STATUS', response.status);
    console.log(json);
})();