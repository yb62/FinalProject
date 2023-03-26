import * as React from 'react';
import { Text, InputGroup, Spinner} from '@blueprintjs/core';
import PlacesAutocomplete, { geocodeByAddress, getLatLng } from 'react-places-autocomplete';


interface Props {
    setPlaceName: (name: string) => void;
}

export const LocationSearchInput: React.FC<Props> = (props: Props) => {
  const [address, setAddress] = React.useState('');

  const handleChange = (address: string) => {
    setAddress(address);
  };

  const handleSelect = (address: string) => {
    geocodeByAddress(address)
      .then((results) => {
        props.setPlaceName(results[0].formatted_address);
        setAddress(results[0].formatted_address);
      });
  };

  return (
    <PlacesAutocomplete value={address} onChange={handleChange} onSelect={handleSelect}>
      {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
        <div>
          <InputGroup {...getInputProps({ placeholder: 'Search Places ...', className: 'location-search-input' })} />
          <div className="autocomplete-dropdown-container">
            {loading && <Text>Loading... {<Spinner/>}</Text>}
            {suggestions.map((suggestion) => {
              const className = suggestion.active ? 'suggestion-item--active' : 'suggestion-item';
              // inline style for demonstration purpose
              const style = suggestion.active
                ? { backgroundColor: '#fafafa', cursor: 'pointer' }
                : { backgroundColor: '#ffffff', cursor: 'pointer' };
              return (
                <div {...getSuggestionItemProps(suggestion, { className, style })} key={suggestion.description}>
                  <Text>{suggestion.description}</Text>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </PlacesAutocomplete>
  )
}