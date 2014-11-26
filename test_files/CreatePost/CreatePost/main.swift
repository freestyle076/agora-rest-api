import Foundation

//create a mutable request with api view path /createuser/, set method to POST
//kyle
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.121:8000/createpost/")!)
//trenton
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/createpost/")!)
request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

//image urls
var imageUrls:[NSURL] = [NSURL(fileURLWithPath: "/Users/kylehandy/Desktop/thisguy.png")!,NSURL(fileURLWithPath: "/Users/kylehandy/Desktop/thisotherguy.png")!]

//formulate imageBase64 array
var imagesBase64:[String] = []
var imageData:NSData
var imageBase64:String
for url in imageUrls{
    imageData = NSData(contentsOfURL:url)!
    imageBase64 = imageData.base64EncodedStringWithOptions(NSDataBase64EncodingOptions(0))
    imagesBase64.append(imageBase64)
}


//parameter values
//common post information
let username = "tmiller12"
let description = "g"
let price = "99"
let title = "Heading Home"
let category = "Furniture"
let gonzaga_email = "1" //boolean contact option
let pref_email = "1" //boolean contact option
let phone = "1" //boolean contact option

//rideshare specific
var departure_date_time = "01 04 2011 16"
var start_location = "Spokane"
var end_location = "Yakima"
var round_trip = "1"
var return_date_time = "01 04 2011 10"

//datelocation specific
var date_time = "01 04 2033 20"
var location = "Spocompton"

//textbook specific
var isbn = "1234213412"

//this is the parameters array that will be formulated as JSON.
//it has space for EVERY attribute of EVERY category.
//only fill attributes that pertain to the category
let params = ["username":username,          //common post information
            "description":description,      // |
            "price":price,                  // |
            "title":title,                  // |
            "category":category,            // |
            "gonzaga_email":gonzaga_email,  // |
            "pref_email":pref_email,        // |
            "phone":phone,                  // <
            "departure_date_time":departure_date_time,  //rideshare specific
            "start_location":start_location,            // |
            "end_location":end_location,                // |
            "round_trip":round_trip,                    // |
            "return_date_time":return_date_time,        // <
            "date_time":date_time,  //datelocation specific
            "location":location,    // <
            "isbn":isbn,        //book specific
            "images":imagesBase64]  //images array
    as Dictionary<String,AnyObject>

/* ITEM POSTS
//prepare parameters for json serialization
var category = "Furniture"
var params = ["username":username, "description":description, "price":price, "title":title, "category":category, "gonzaga_email":gonzaga_email, "pref_email":pref_email, "phone":phone, "images":imagesBase64] as Dictionary<String,AnyObject>
*/

/* RIDESHARE POST
//prepare parameters for json serialization
var category = "Rideshare"
var params = ["username":username, "description":description, "price":price, "title":title, "category":category, "gonzaga_email":gonzaga_email, "pref_email":pref_email, "phone":phone, "return_date_time":return_date_time, "end_location":end_location, "start_location":start_location, "round_trip":round_trip, "departure_date_time":departure_date_time,"images":imagesBase64] as Dictionary<String,AnyObject>
*/

/* DATELOCATION POST
//prepare parameters for json serialization
var category = "Events"
var params = ["username":username, "description":description, "price":price, "title":title, "category":category, "gonzaga_email":gonzaga_email, "pref_email":pref_email, "phone":phone, "date_time":return_date_time, "location":location,"images":imagesBase64] as Dictionary<String,AnyObject>
*/

/* TEXTBOOK POST
//prepare parameters for json serialization
var category = "Books"
var params = ["username":username, "description":description, "price":price, "title":title, "category":category, "gonzaga_email":gonzaga_email, "pref_email":pref_email, "phone":phone, "isbn":isbn, "images":imagesBase64] as Dictionary<String,AnyObject>
*/





//Load body with JSON serialized parameters, set headers for JSON! (Star trek?)
var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")


//define NSURLSession data task with completionHandler call back function
var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
    
    println(response)
    
    //read the message from the response
    var message = ""
    var json = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? NSDictionary
    if(err != nil) {
        println(err!.localizedDescription)
        let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
        println("Error could not parse JSON: '\(jsonStr)'")
    }
    else{
        if let parseJSON = json as? Dictionary<String,AnyObject>{
            message = parseJSON["message"] as String
        }
    }
    
    //downcast NSURLResponse object to NSHTTPURLResponse
    if let httpResponse = response as? NSHTTPURLResponse {
        
        //get the status code
        var status_code = httpResponse.statusCode
        
        //200 = OK: user created, carry on!
        if(status_code == 200){
            println(message)
        }
            
        //400 = BAD_REQUEST: error in creating user, display error!
        else if(status_code == 400){
            println(message)
        }
            
        //500 = INTERNAL_SERVER_ERROR. Oh snap *_*
        else if(status_code == 500){
            println("The server is down! Call the fire department!")
        }
        
        
    } else {
        println("Error in casting response, data incomplete")
    }

    
    
})

task.resume()


sleep(5)

