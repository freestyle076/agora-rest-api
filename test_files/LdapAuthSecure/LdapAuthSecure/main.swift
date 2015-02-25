//
//  main.swift
//  LdapAuthSecure
//
//  Created by Kyle Handy on 1/26/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//


import Foundation

class SecureLogin: NSObject, NSURLSessionDelegate {
    
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
                delegateQueue:nil)
            
            
            var task = session.dataTaskWithRequest(request,callback)
            
            
            task.resume()
            println("task resume")
    }
    
    
    func URLSession(session: NSURLSession, didReceiveChallenge challenge: NSURLAuthenticationChallenge, completionHandler: (NSURLSessionAuthChallengeDisposition, NSURLCredential!) -> Void) {
        println("Challenge Received****")
        completionHandler(NSURLSessionAuthChallengeDisposition.UseCredential, NSURLCredential(forTrust: challenge.protectionSpace.serverTrust))
        
    }
    
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
                
                let username = parseJSON["username"] as String
                let first_name = parseJSON["first_name"] as String
                let last_name = parseJSON["last_name"] as String
                
                let g_email = parseJSON["g_email"] as String
                let p_email = parseJSON["p_email"] as String //empty string if none available
                let phone = parseJSON["phone"] as String     //empty string if none available
                let exists = parseJSON["exists"] as String   //yes or no
                
                println(first_name)
                println(exists)
                println(username)
                println(phone)
                
            }
        }
    }
})


println("beginning wait")

sleep(25)