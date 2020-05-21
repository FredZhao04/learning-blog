// index.js
// 获取应用实例
const app = getApp()

Page({
    isLoaded: false,

    data: {
      schedules: [],
      openid:null,
    },

    // 应用初始化检查登录态
    onLoad () {
      let that = this;

      if (!app.globalData.openid) {
        app.openidReadyCallback = res => {
          console.log(res)
          that.setData({
            openid: res.result.openid
          })
          that.getSchedules(res.result.openid)
        }
      }else{
        that.getSchedules(app.globalData.openid)
      }

      
    },

    // onShow 的时候获取相册列表
    onShow() {
      
    },

    // 获取日程列表
    getSchedules(openid){
      let that = this;
      const db = wx.cloud.database({})
      db.collection('schedules').where({openid:openid}).get().then(res => {
        console.log(res)
        that.setData({
          schedules: res.data
        })
      }) 
    
    },
})
