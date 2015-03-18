//
//  AgoraRequester.swift
//  AgoraRequesterTester
//
//  Created by Kyle Handy on 2/10/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation
import SystemConfiguration

class AgoraRequester: NSObject, NSURLSessionDelegate {
    
    //base URL
    let baseURLst: String
    
    //base HTTPS url
    let baseHTTPSURLst: String
    
    //Configuration for created NSURLSessions
    let seshConfig: NSURLSessionConfiguration
    
    //default initializer, specifies the target URL
    override init(){
        self.baseURLst  = "https://cs-design:8001/"
        self.baseHTTPSURLst = "https://cs-design:8001/"
        self.seshConfig = NSURLSessionConfiguration.defaultSessionConfiguration()
        seshConfig.timeoutIntervalForRequest = 60
        super.init()
    }
    
    func POST(route: String, params: Dictionary<String,AnyObject>, success: ((Dictionary<String,AnyObject>) -> Void)?, failure: ((Int,String) -> Void)?){
        
        //instantiate the session
        var session = NSURLSession(configuration: self.seshConfig)
        
        //check for network connection
        if Reachability.isConnectedToNetwork(){
            
            //init request, set target URL
            var request = NSMutableURLRequest(URL: NSURL(string: self.baseURLst + route)!)
            
            //request headers: JSON -> and <-
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            //AgoraRequest.POST uses method POST
            request.HTTPMethod = "POST"
            
            //load up JSON object into request body
            request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: nil)
            
            //form the task, use passed callback function
            var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
                
                //error is not nil means there was a timeout
                if error != nil{
                    if failure != nil{
                        failure!(599,"599 connection timeout")
                    }
                }
                
                //else proceed...
                else if let httpResponse = response as? NSHTTPURLResponse{
                    
                    let status_code = httpResponse.statusCode
                    
                    //200 OK, continue as planned
                    if status_code == 200 {
                        
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                        
                        //error parsing
                        if err != nil {
                            //error function: 500 server failure in forming response
                            if failure != nil {
                                failure!(500,"500 server error")
                            }
                        }
                        
                        //if callback provided run callback function with provided JSON results
                        else if success != nil {
                            success!(parseJSON!)
                        }
                        
                    }
                    
                    //400 Bad Request, get error message
                    else if status_code == 400 {
                        
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                        
                        //error function: 400 bad request by client
                        if failure != nil {
                            let message = parseJSON!["message"] as String
                            failure!(400,message)
                        }
                    }
                    
                    //500 server failure
                    else if status_code == 500 {
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500,"500 server error")
                        }
                    }
                }
                else{
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500,"500 server error")
                    }
                }
            })
            
            task.resume()
            
        }
            
        //else no network connection
        else{
            //error function: 58 no connection
            if failure != nil {
                failure!(58,"58 no internet connection")
            }
        }
        
    }
    
    func LdapAuth(username: String, password: String, success: ((Dictionary<String,AnyObject>) -> Void)?, failure: ((Int,String) -> Void)?, badCreds: (Void -> Void)?){
        
        //check for network connection
        if Reachability.isConnectedToNetwork(){
        
            var request = NSMutableURLRequest(URL: NSURL(string: self.baseHTTPSURLst + "ldapauth/")!)
            request.HTTPMethod = "POST"
            
            
            var params = ["username":username, "password":password] as Dictionary<String, String>
            
            var err: NSError?
            request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            
            var session = NSURLSession(configuration: NSURLSessionConfiguration.defaultSessionConfiguration(),
                delegate: self,
                delegateQueue:nil)
            
            
            var task = session.dataTaskWithRequest(request,completionHandler: {data, response, error -> Void in
                
                println("in completion handler")
                
                //error is not nil means unresponsive server (dead or timeout)
                if error != nil{
                    if failure != nil{
                        failure!(599,"599 connection timeout")
                    }
                }
                    
                //else proceed...
                else if let httpResponse = response as? NSHTTPURLResponse{
                    
                    
                    let status_code = httpResponse.statusCode
                    
                    //200 OK, continue as planned
                    if status_code == 200 {
                        println(200)
                        
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                        
                        //error parsing
                        if err != nil {
                            
                            //error function: 500 server failure in forming response
                            if failure != nil {
                                let message = parseJSON!["message"] as String
                                failure!(500,message)
                            }
                        }
                            
                        //if callback provided run callback function with provided JSON results
                        else if success != nil {
                            success!(parseJSON!)
                        }
                        
                    }
                        
                    //400 Bad Request, get error message
                    else if status_code == 400 {
                        println(400)
                        //error function: 400 bad request by client
                        if badCreds != nil {
                            println("400 bad request by client")
                            badCreds!()
                        }
                    }
                        
                        //500 server failure
                    else if status_code == 500 {
                        println(500)
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500,"500 server failure by status code")
                        }
                    }
                    else{
                        println(status_code)
                        println("final else")
                    }
                }
                else{
                    println(500)
                    println("could not cast")
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500,"500 server failure by response body")
                    }
                }
            })
            
            task.resume()
            println("task resume")
        }
        //else no network connection
        else{
            //error function: 58 no connection
            if failure != nil {
                failure!(58,"58 no connection")
            }
        }
    
    }
    
    func URLSession(session: NSURLSession, didReceiveChallenge challenge: NSURLAuthenticationChallenge, completionHandler: (NSURLSessionAuthChallengeDisposition, NSURLCredential!) -> Void) {
        println("challenge")
        completionHandler(NSURLSessionAuthChallengeDisposition.UseCredential, NSURLCredential(forTrust: challenge.protectionSpace.serverTrust))
        
        
    }
    
}


//Reachability class will tell us if there is a network connection
public class Reachability {
    
    class func isConnectedToNetwork() -> Bool {
        
        var zeroAddress = sockaddr_in(sin_len: 0, sin_family: 0, sin_port: 0, sin_addr: in_addr(s_addr: 0), sin_zero: (0, 0, 0, 0, 0, 0, 0, 0))
        zeroAddress.sin_len = UInt8(sizeofValue(zeroAddress))
        zeroAddress.sin_family = sa_family_t(AF_INET)
        
        let defaultRouteReachability = withUnsafePointer(&zeroAddress) {
            SCNetworkReachabilityCreateWithAddress(nil, UnsafePointer($0)).takeRetainedValue()
        }
        
        var flags: SCNetworkReachabilityFlags = 0
        if SCNetworkReachabilityGetFlags(defaultRouteReachability, &flags) == 0 {
            return false
        }
        
        let isReachable = (flags & UInt32(kSCNetworkFlagsReachable)) != 0
        let needsConnection = (flags & UInt32(kSCNetworkFlagsConnectionRequired)) != 0
        
        return (isReachable && !needsConnection) ? true : false
    }
    
}
