# Api documentation

##Making requests
All queries to the  API must be served over HTTPS and need to be presented in this form: 

`https://<host>/api?url1="<url1>"&url2="<url2>"url3="<url3>"&days=<days>`

Like this for example:

`https://link-shorter-v2.herokuapp.com/api?url1="google.com"`
response:
`{"code": 200, "message": "You enter 1 links and 1 of them is valid", "links": ["link-shorter-v2.herokuapp.com/65M3JD"], "active_until": "2020-02-08 01:48:47.438330"}`

We support only GET HTTP methods.

There are two Parameter(`url` and `days`)

`url` - Required. You can write a lot of links using parameters url1, url2, ... urlN

`days` - Optional. Default value 90. Integer. Days until Expiration date. it should be more than 0 and less than 367
