import Foundation

//create a mutable request with api view path /editpost/, set method to POST
//server
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.3:8000/editpost/")!)


//trenton
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/editpost/")!)

request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

//image urls
var imageUrls:[NSURL] = [NSURL(fileURLWithPath: "/Users/trentonmiller/Desktop/Seahawk.png")!,NSURL(fileURLWithPath: "/Users/trentonmiller/Desktop/Seahawk.png")!,NSURL(fileURLWithPath: "/Users/trentonmiller/Desktop/Seahawk.png")!]
//var imageUrls:[NSURL] = []


//formulate imageBase64 array
var imagesBase64:[String] = []
var imageData:NSData
var imageBase64:String
for url in imageUrls{
    imageData = NSData(contentsOfURL:url)!
    imageBase64 = imageData.base64EncodedStringWithOptions(NSDataBase64EncodingOptions(0))
    imagesBase64.append(imageBase64)
}
imagesBase64.append("")
// Category must match previous category, thus, it cannot change
let category = "Services"
let id = "36"


//parameter values
//common post information
let description = "AI"
let price = "0"
let title = "Coming North"

//Image values
//Empty String signifies non alteration of Image, "delete" signifies the image was deleted
//Image data signifies a change in the image.
imagesBase64[0] = "deleted"
imagesBase64[1] = ""

//contact options
let gonzaga_email = "1" //boolean contact option
let pref_email = "1" //boolean contact option
let phone = "1" //boolean contact option
let text = "1" //boolean contact option

//rideshare specific
var departure_date_time = "01/04/15, 5:30 AM"
var start_location = "LA"
var end_location = "Spokane"
var round_trip = "0"
var return_date_time = "01/04/15, 10:30 PM"

//datelocation specific
var date_time = "01/20/15, 9:30 PM"
var location = "My House"

//textbook specific
var isbn = "1234213412"

//this is the parameters array that will be formulated as JSON.
//it has space for EVERY attribute of EVERY category.
//only fill attributes that pertain to the category
let params = ["post_id":id,                        // |
    "description":description,      // |
    "price":price,                  // |
    "title":title,                  // |
    "category":category,            // |
    "gonzaga_email":gonzaga_email,  // |
    "pref_email":pref_email,        // |
    "call":phone,                  // |
    "text":text,                    // <
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


//Load body with JSON serialized parameters, set headers for JSON! (Star trek?)
var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")


//define NSURLSession data task with completionHandler call back function
var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
    
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
            message = parseJSON["message"]! as String
        }
    }
    
    //downcast NSURLResponse object to NSHTTPURLResponse
    if let httpResponse = response as? NSHTTPURLResponse {
        
        //get the status code
        var status_code = httpResponse.statusCode
        
        //200 = OK: user created, carry on!
        if(status_code == 200){
            println(message)
            println(id)
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

