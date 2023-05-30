import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { supabase } from './supabaseClient'
import { useSearchParams } from 'react-router-dom'

function App() {
  const [ searchParams, _ ] = useSearchParams()
  const [images, setImages] = useState([])
  useEffect(() => {
    supabase.from('photos').select("*").eq("location_id", searchParams.get('location')).then(({data, error}) => {
      setImages(data)
    })
    return () => {}
  }, [searchParams])

  if (!searchParams.get('location')) {
    return <span>Page not found</span>
  }
  return (
    <>
      {images.map(image => {
        return (
          <img key={image.id} src={image.url}>
          </img>
        );
      })}
    </>
  )
}

export default App
