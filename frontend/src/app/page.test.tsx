import * as React from 'react'
import {render, screen}  from '@testing-library/react'
import HomePage from './page'
 
describe("screen rendering", () =>{
  it('renders correctly', () => {
    const tree = render(<HomePage />)
    const headingElement = screen.getByText("Yes Sir I Can Boogie")
  })
})