import * as React from 'react'
import HomePage from './page'
import renderer from 'react-test-renderer'
 
it('renders correctly', () => {
  const tree = renderer.create(<HomePage />).toJSON()
  expect(tree).toMatchSnapshot()
})