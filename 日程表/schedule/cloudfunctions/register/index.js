// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init({
  // API 调用都保持和云函数当前所在环境一致
  env: cloud.DYNAMIC_CURRENT_ENV
})

// 云函数入口函数
/**
 * 根据 openid 查找数据库中是否存在该用户，不存在的话就添加其openid、昵称和头像链接
 * 
 * event 参数包含小程序端调用传入的 data
 * 
 */
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()

  const db = cloud.database()

  try{
    await db.collection('user').where({ openid: wxContext.OPENID}).get().then(res => {
      if(res.data.length == 0){
        db.collection('user').add({
          data: {
            openid: wxContext.OPENID,
            avatarUrl: event.avatarUrl,
            nickName: event.nickName
          }
        })
      }
    })
  } catch(e){
    console.log(e)
  }

  return {
    event,
    openid: wxContext.OPENID,
    appid: wxContext.APPID,
    unionid: wxContext.UNIONID,
  }
}