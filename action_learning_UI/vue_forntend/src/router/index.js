import { createRouter, createWebHistory } from "vue-router"

import Home from '../views/Home'
import About from '../views/About'
import UploadRefvideo from  '../views/UploadRefvideo'
import Multiple from  '../views/Multiple'

const routes=[
    {
        path:'/home',
        name:'Home',
        component:Home
    },
    {
        path:"/about",
        name:'About',
        component:About,

    },
    {
        path:'/uploadrefvideo',     
        name:'UploadRefvideo',
        component:UploadRefvideo,        

    },
    {
        path:'/multiple_person',
        name:'Multiple',
        component:Multiple,
    }
]

const router= createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})


export default router