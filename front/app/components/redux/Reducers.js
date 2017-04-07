let initialDetailState = {
  source: undefined,
  owner: undefined,
  height: undefined
};

export function detail (state = initialDetailState, action) {
  switch (action.type) {
    // On showing the detail view
    case 'DID_SHOW_DETAIL':
      return {
        ...state,
        source: action.source
      };
    // Default, catch all
    default:
      return state;
  }
}
