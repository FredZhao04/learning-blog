//app.js
App({
    onLaunch () {
        // 初始化云函数
        wx.cloud.init({
          env:'homework-bc9ec9',
          traceUser: true
        })

        if(!this.globalData.openId){
          this.toLogin()
        }
        
        // 获取用户信息
        wx.getSetting({
            success: res => {
                if (res.authSetting['scope.userInfo']) {
                    // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
                    wx.getUserInfo({
                        success: res => {
                            this.globalData.userInfo = res.userInfo

                            // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
                            // 所以此处加入 callback 以防止这种情况
                            if (this.userInfoReadyCallback) {
                                this.userInfoReadyCallback(res)
                            }
                        }
                    })
                } else {
                    // 跳转登录页面让用户登录
                    wx.switchTab({ url: '../../pages/user/user' })
                }
            }
        })
    },
//获取用户的openid
    toLogin(){
      wx.cloud.callFunction({
        name: 'login',
        complete: res => {
          this.globalData.openid = res.result.openid

          if (this.openidReadyCallback) {
            this.openidReadyCallback(res)
          }
        }
      })
    },
  
    globalData: {
        hasUser: false, // 数据库中是否有用户
        hasUserInfo: false, // 小程序的userInfo是否有获取
        userInfo: null,
        code: null,
        openid: null,
        nickName: ''
    }
})
