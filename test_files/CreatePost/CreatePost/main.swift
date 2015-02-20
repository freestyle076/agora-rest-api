import Foundation

//create a mutable request with api view path /createupost/, set method to POST
//server
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.3:8000/createpost/")!)

//kyle
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/createpost/")!)


//trenton
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/createpost/")!)

request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

//image urls

//var imageUrls:[NSURL] = []
var imageUrls:[NSURL] = [NSURL(fileURLWithPath: "/Users/trentonmiller/Desktop/Seahawk.png")!,NSURL(fileURLWithPath: "/Users/trentonmiller/Desktop/Seahawk.png")!,NSURL(fileURLWithPath: "/Users/trentonmiller/Desktop/Seahawk.png")!]



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
let description = "Deleted Pictures"
let price = "5"
let title = "Gameshows 101"
let category = "Services"


let gonzaga_email = "1" //boolean contact option
let pref_email = "1" //boolean contact option
let phone = "1" //boolean contact option
let text = "1" //boolean contact option

//rideshare specific
var departure_date_time = ""
var start_location = ""
var end_location = ""
var round_trip = "1"
var return_date_time = ""


//datelocation specific
//var date_time = "01/20/15, 9:30 PM"
var date_time = "01/04/15, 10:30 PM"
var location = "My House"

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
    //downcast NSURLResponse object to NSHTTPURLResponse
    if let httpResponse = response as? NSHTTPURLResponse {
        
        //get the status code
        var status_code = httpResponse.statusCode
        
        //200 = OK: carry on!
        if(status_code == 200){
            
            var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
            if(err != nil) {
                println(err!.localizedDescription)
                let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
                println("Error could not parse JSON: '\(jsonStr)'")
            }
                
            else {
                
                //response code is OK, continue with parsing JSON and reading response data
                //THIS IS WHERE RESPONSE HANDLING CODE SHOULD GO
        
            }
        }
            
            //400 = BAD_REQUEST: error in creating user, display error!
        else if(status_code == 400){
            var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
            if(err != nil) {
                println(err!.localizedDescription)
                let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
                println("Error could not parse JSON: '\(jsonStr)'")
            }
            else{

            }
        }
            
            //500 = INTERNAL_SERVER_ERROR. Oh snap *_*
        else if(status_code == 500){
            println("The server is down! I blame Schnagl")
        }
        
        
    }
    else {
        println("Error in casting response, data incomplete")
    }

    
    
})

task.resume()


sleep(5)

