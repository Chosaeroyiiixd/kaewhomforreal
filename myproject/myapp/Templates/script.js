const changeBackground = () => {
    if(window.scrollY >= 80){
        setnav(true)
    }else{
        setnav(false)
    }
};

window.addEventListener('scroll', changeBackground);