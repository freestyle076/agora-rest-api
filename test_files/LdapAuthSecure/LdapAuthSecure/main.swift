//
//  main.swift
//  LdapAuthSecure
//
//  Created by Kyle Handy on 1/26/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//


import Foundation

class SecureLogin: NSObject, NSURLSessionDelegate, NSURLSessionTaskDelegate {
    
    func attemptLogin(username: String, password: String,
        callback: ((NSData!,NSURLResponse!,NSError!) -> Void)?) {
            
            println("inside attempt login")
            
            var request = NSMutableURLRequest(URL: NSURL(string: "https://147.222.164.91:8000/ldapauth/")!)
            request.HTTPMethod = "POST"

            
            var params = ["username":username, "password":password] as Dictionary<String, String>
            
            var err: NSError?
            request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            var configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
            var session = NSURLSession(configuration: configuration,
                delegate: self,
                delegateQueue:NSOperationQueue.mainQueue())
            var task = session.dataTaskWithRequest(request,callback)
            
            task.resume()
    }
    
    /*
    func URLSession(session: NSURLSession,
        task: NSURLSessionTask,
        didReceiveChallenge challenge: NSURLAuthenticationChallenge,
        completionHandler: (NSURLSessionAuthChallengeDisposition,NSURLCredential!) -> Void) {
            println("Challenge received")
            completionHandler(NSURLSessionAuthChallengeDisposition.UseCredential, NSURLCredential(forTrust: challenge.protectionSpace.serverTrust))
    }
    
    func URLSession(session: NSURLSession,
        task: NSURLSessionTask,
        willPerformHTTPRedirection response: NSHTTPURLResponse,
        newRequest request: NSURLRequest,
        completionHandler: (NSURLRequest!) -> Void) {
            println("Redirection received")
            var newRequest : NSURLRequest? = request
            println(newRequest?.description)
            completionHandler(newRequest)
    }*/
}

var username = "khandy"

var password = "Rusty3220"

var gatekeeper = SecureLogin()

gatekeeper.attemptLogin(username, password: password, callback: {data, response, error -> Void in
    
    println("inside gatekeeper")
    
    //get the status code of the response
    var status_code = (response as NSHTTPURLResponse).statusCode
    
    //react according to status code
    if status_code == 200 {
        
        var jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
        var err: NSError?
        var json = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? NSDictionary
        
        //check for error in deserialization
        if(err != nil) {
            println(err!.localizedDescription)
            let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
            println("Error could not parse JSON: '\(jsonStr)'")
        }
            //else parse JSON and receive user data values
        else {
            //parse JSON for data values
            if let parseJSON = json as? Dictionary<String,AnyObject>{
                
                let username = parseJSON["username"]
                let first_name = parseJSON["first_name"]
                let last_name = parseJSON["last_name"]
                
                let g_email = parseJSON["g_email"]
                let p_email = parseJSON["p_email"]  //empty string if none available
                let phone = parseJSON["phone"]      //empty string if none available
                let exists = parseJSON["exists"]    //yes or no
                
                println(first_name)
                
                let posts: AnyObject = parseJSON["posts"]!
                if posts.length > 0{
                    
                    //iterate through each post
                    for i in 0...(posts.count - 1){
                        let post: AnyObject! = posts[i] //just so we don't keep re-resolving this reference
                        
                        //get the easy ones, title, display_value and post ID
                        let title = post["title"] as String
                        let display_value = post["display_value"]! as String
                        let postID = post["id"]! as Int
                        
                        
                        //read imageString, base64 encoded
                        let imageString = post["image"]! as String
                        
                        //make sure there is an image...
                        if !imageString.isEmpty {
                            let imageData = NSData(base64EncodedString: imageString, options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                            
                            //THIS IS WHERE IMAGES ARE HANDLED, if there are any...
                        }
                            
                            //no image included...
                        else{
                            //NO IMAGE WITH POST
                        }
                    }
                }
            }
        }
    }
})


println("beginning wait")

sleep(25)