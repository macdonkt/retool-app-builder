# Widget & Query Catalog

Auto-generated from `transit_patterns.json`. Use this for quick lookup.
**For the full field structure, always read transit_patterns.json directly.**

- **95 widget types**
- **5 query types**
- **7 state templates**
- **5 frame templates**
- **46 event patterns**

---
## Widget Types

### AgentChatWidget
- Example ID: `agentChat1`
- Total fields: **16**
- Key configurable fields: `hidden`

| Field | Default |
|-------|---------|
| `hidden` | `false` |

### AlertWidget2
- Example ID: `alert1`
- Total fields: **26**
- Key configurable fields: `hidden`, `value`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `"info"` |
| `events` | `{...0 keys}` |

### AuthLoginWidget
- Example ID: `authLogin1`
- Total fields: **3**
- Key configurable fields: `label`

| Field | Default |
|-------|---------|
| `label` | `""` |

### AvatarGroupWidget
- Example ID: `avatarGroup1`
- Total fields: **11**
- Key configurable fields: `hidden`

| Field | Default |
|-------|---------|
| `hidden` | `false` |

### AvatarWidget
- Example ID: `avatar1`
- Total fields: **18**
- Key configurable fields: `src`, `hidden`, `label`, `events`

| Field | Default |
|-------|---------|
| `src` | `"{{ current_user.profilePhotoUrl }}"` |
| `hidden` | `false` |
| `label` | `"{{ current_user.fullName }}"` |
| `events` | `{...0 keys}` |

### BoundingBoxWidget
- Example ID: `boundingBox1`
- Total fields: **5**

### BreadcrumbsWidget
- Example ID: `breadcrumbs1`
- Total fields: **33**
- Key configurable fields: `hidden`, `data`, `value`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"{{ retoolContext.appUuid }}"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### ButtonGroupWidget2
- Example ID: `buttonGroup1`
- Total fields: **23**
- Key configurable fields: `hidden`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `events` | `{...0 keys}` |

### ButtonWidget2
- Example ID: `button1`
- Total fields: **20**
- Key configurable fields: `hidden`, `text`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `text` | `"Button"` |
| `events` | `[1 items]` |
| `disabled` | `false` |

### CalendarInputWidget
- Example ID: `calendarInput1`
- Total fields: **26**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `"{{ new Date() }}"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### CalendarWidget2
- Example ID: `calendar1`
- Total fields: **48**
- Key configurable fields: `hidden`, `data`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `[0 items]` |
| `events` | `{...0 keys}` |

### CascaderWidget2
- Example ID: `cascader1`
- Total fields: **67**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `null` |
| `placeholder` | `"Select an option"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### ChartWidget2
- Example ID: `mixedChart1`
- Total fields: **160**
- Key configurable fields: `hidden`, `data`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `null` |
| `events` | `{...0 keys}` |

### ChatWidget
- Example ID: `llmChat1`
- Total fields: **46**
- Key configurable fields: `hidden`, `data`, `value`, `placeholder`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `""` |
| `placeholder` | `"Type a message"` |
| `events` | `[3 items]` |

### CheckboxGroupWidget2
- Example ID: `checkboxGroup1`
- Total fields: **59**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"{{ [self.values[0]] }}"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### CheckboxWidget2
- Example ID: `checkbox1`
- Total fields: **22**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `false` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### ColorInputWidget
- Example ID: `colorInput1`
- Total fields: **34**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `"{{ theme.primary }}"` |
| `placeholder` | `"Enter a color"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### CommentThreadWidget
- Example ID: `commentThread1`
- Total fields: **30**
- Key configurable fields: `hidden`, `data`, `value`, `placeholder`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `""` |
| `placeholder` | `"Type a message"` |
| `events` | `[1 items]` |

### ContainerWidget2
- Example ID: `container1`
- Total fields: **50**
- Key configurable fields: `hidden`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### DateRangeWidget
- Example ID: `dateRange1`
- Total fields: **36**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `{...2 keys}` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### DateTimeWidget
- Example ID: `dateTime1`
- Total fields: **43**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `"{{ new Date() }}"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### DateWidget
- Example ID: `date1`
- Total fields: **35**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `"{{ new Date() }}"` |
| `label` | `"Label"` |
| `events` | `[1 items]` |
| `disabled` | `false` |

### DividerWidget
- Example ID: `divider1`
- Total fields: **7**
- Key configurable fields: `hidden`, `text`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `text` | `""` |

### DropdownButtonWidget
- Example ID: `dropdownButton1`
- Total fields: **32**
- Key configurable fields: `hidden`, `data`, `text`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `[0 items]` |
| `text` | `"Menu"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### EditableNumberWidget
- Example ID: `editableNumber1`
- Total fields: **42**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `null` |
| `placeholder` | `"Enter value"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |

### EditableTextAreaWidget
- Example ID: `editableTextArea1`
- Total fields: **37**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `""` |
| `placeholder` | `"Enter value"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### EditableTextWidget2
- Example ID: `editableText1`
- Total fields: **41**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `""` |
| `placeholder` | `"Enter value"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |

### FileButtonWidget
- Example ID: `fileButton1`
- Total fields: **36**
- Key configurable fields: `hidden`, `text`, `value`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `text` | `"Browse"` |
| `value` | `[0 items]` |
| `events` | `[0 items]` |
| `disabled` | `false` |

### FileDropzoneWidget
- Example ID: `fileDropzone1`
- Total fields: **40**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `[0 items]` |
| `placeholder` | `"Select or drag and drop"` |
| `label` | `""` |
| `events` | `[0 items]` |
| `disabled` | `false` |

### FileInputWidget
- Example ID: `fileInput1`
- Total fields: **44**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `[0 items]` |
| `placeholder` | `"No file selected"` |
| `label` | `"Label"` |
| `events` | `[0 items]` |
| `disabled` | `false` |

### FilterWidget
- Example ID: `filter1`
- Total fields: **10**
- Key configurable fields: `hidden`, `value`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `null` |

### FormWidget2
- Example ID: `form1`
- Total fields: **30**
- Key configurable fields: `hidden`, `data`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `{...0 keys}` |
| `events` | `[2 items]` |
| `disabled` | `false` |

### HTMLWidget
- Example ID: `html1`
- Total fields: **9**
- Key configurable fields: `hidden`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `events` | `{...0 keys}` |

### IFrameWidget2
- Example ID: `iFrame1`
- Total fields: **21**
- Key configurable fields: `src`, `hidden`

| Field | Default |
|-------|---------|
| `src` | `"https://www.wikipedia.org/"` |
| `hidden` | `false` |

### IconTextWidget
- Example ID: `iconText1`
- Total fields: **12**
- Key configurable fields: `hidden`, `text`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `text` | `"Hello {{ current_user.firstName || 'f..."` |
| `events` | `{...0 keys}` |

### IconWidget
- Example ID: `icon1`
- Total fields: **13**
- Key configurable fields: `hidden`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### ImageGridWidget
- Example ID: `imageGrid1`
- Total fields: **24**
- Key configurable fields: `hidden`, `data`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `[0 items]` |
| `events` | `{...0 keys}` |

### ImageWidget2
- Example ID: `image1`
- Total fields: **24**
- Key configurable fields: `src`, `hidden`, `events`

| Field | Default |
|-------|---------|
| `src` | `"https://picsum.photos/id/1025/800/600"` |
| `hidden` | `false` |
| `events` | `{...0 keys}` |

### JSONEditorWidget
- Example ID: `jsonEditor1`
- Total fields: **3**
- Key configurable fields: `value`

| Field | Default |
|-------|---------|
| `value` | `"{
  "a": {
    "b": [1,2,3,4,5,6,7,8,..."` |

### JSONExplorerWidget
- Example ID: `jsonExplorer1`
- Total fields: **4**
- Key configurable fields: `value`

| Field | Default |
|-------|---------|
| `value` | `"{
  "a": {
    "b": [1,2,3,4,5,6,7,8,..."` |

### JSONSchemaFormWidget
- Example ID: `jsonSchemaForm1`
- Total fields: **11**
- Key configurable fields: `data`

| Field | Default |
|-------|---------|
| `data` | `"{
  "username": "john.doe",
  "passwo..."` |

### KeyValueWidget2
- Example ID: `keyValue1`
- Total fields: **27**
- Key configurable fields: `hidden`, `data`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `"{
  id: 0,
  firstName: 'Chic',
  las..."` |
| `events` | `{...0 keys}` |

### LinkListWidget
- Example ID: `linkList1`
- Total fields: **35**
- Key configurable fields: `hidden`, `data`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `[0 items]` |
| `label` | `""` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### LinkWidget
- Example ID: `link1`
- Total fields: **18**
- Key configurable fields: `hidden`, `text`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `text` | `"Link"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### ListViewWidget2
- Example ID: `listView1`
- Total fields: **21**
- Key configurable fields: `hidden`, `data`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `"[0, 1, 2, 3, 4, 5]"` |

### ListboxWidget
- Example ID: `listbox1`
- Total fields: **59**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"{{ self.values[0] }}"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### LookerWidget
- Example ID: `looker1`
- Total fields: **1**

### MapWidget
- Example ID: `mapboxMap1`
- Total fields: **18**

### MicrophoneWidget2
- Example ID: `microphone1`
- Total fields: **13**
- Key configurable fields: `hidden`, `label`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `label` | `"Record"` |
| `events` | `{...0 keys}` |

### MultiselectListboxWidget
- Example ID: `multiselectListbox1`
- Total fields: **61**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"{{ [self.values[0]] }}"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### MultiselectWidget2
- Example ID: `multiselect1`
- Total fields: **76**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `[0 items]` |
| `placeholder` | `"Select options"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### NavigationWidget2
- Example ID: `navigation1`
- Total fields: **57**
- Key configurable fields: `src`, `hidden`, `data`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `src` | `"data:image/svg+xml,%3csvg%20width='70..."` |
| `hidden` | `false` |
| `data` | `"{{ retoolContext.pages }}"` |
| `events` | `[1 items]` |
| `disabled` | `false` |

### NumberInputWidget
- Example ID: `numberInput1`
- Total fields: **43**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `0` |
| `placeholder` | `"Enter value"` |
| `label` | `"Label"` |
| `events` | `[1 items]` |
| `disabled` | `false` |

### PDFViewerWidget2
- Example ID: `pdf1`
- Total fields: **16**
- Key configurable fields: `src`, `hidden`

| Field | Default |
|-------|---------|
| `src` | `"https://upload.wikimedia.org/wikipedi..."` |
| `hidden` | `false` |

### PageInputWidget
- Example ID: `pageInput1`
- Total fields: **12**
- Key configurable fields: `hidden`, `value`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `1` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### PaginationWidget
- Example ID: `pagination1`
- Total fields: **9**
- Key configurable fields: `hidden`, `value`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `1` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### PasswordInputWidget
- Example ID: `password1`
- Total fields: **35**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `""` |
| `placeholder` | `"••••••••••"` |
| `label` | `"Password"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### PhoneNumberInputWidget
- Example ID: `phoneNumber1`
- Total fields: **34**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `""` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### ProgressBarWidget
- Example ID: `progressBar1`
- Total fields: **15**
- Key configurable fields: `hidden`, `value`, `label`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `60` |
| `label` | `""` |

### ProgressCircleWidget
- Example ID: `progressCircle1`
- Total fields: **9**
- Key configurable fields: `hidden`, `value`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `60` |

### QRCodeWidget
- Example ID: `qrCode1`
- Total fields: **8**
- Key configurable fields: `hidden`, `value`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `"https://retool.com"` |

### RadioGroupWidget2
- Example ID: `radioGroup1`
- Total fields: **47**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"{{ self.values[0] }}"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### RangeSliderWidget
- Example ID: `rangeSlider1`
- Total fields: **27**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `{...2 keys}` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### RatingWidget2
- Example ID: `rating1`
- Total fields: **26**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `4.5` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### ReorderableListWidget
- Example ID: `reorderableList1`
- Total fields: **3**
- Key configurable fields: `value`

| Field | Default |
|-------|---------|
| `value` | `"['The first card', 'The second card',..."` |

### ScannerWidget2
- Example ID: `scanner1`
- Total fields: **11**
- Key configurable fields: `hidden`, `data`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `[0 items]` |
| `events` | `{...0 keys}` |

### SegmentedControlWidget
- Example ID: `segmentedControl1`
- Total fields: **41**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"{{ self.values[0] }}"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### SelectWidget2
- Example ID: `select1`
- Total fields: **71**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `null` |
| `placeholder` | `"Select an option"` |
| `label` | `"Label"` |
| `events` | `[1 items]` |
| `disabled` | `false` |

### SignaturePad2
- Example ID: `signature1`
- Total fields: **24**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `""` |
| `label` | `""` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### SliderWidget2
- Example ID: `slider1`
- Total fields: **27**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `2` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### SpacerWidget
- Example ID: `spacer1`
- Total fields: **4**
- Key configurable fields: `hidden`

| Field | Default |
|-------|---------|
| `hidden` | `false` |

### SplitButtonWidget
- Example ID: `splitButton1`
- Total fields: **33**
- Key configurable fields: `hidden`, `data`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `[0 items]` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### StatisticWidget2
- Example ID: `statistic1`
- Total fields: **33**
- Key configurable fields: `hidden`, `value`, `label`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `7552.8` |
| `label` | `"Gross volume"` |
| `events` | `{...0 keys}` |

### StatusWidget
- Example ID: `status1`
- Total fields: **27**
- Key configurable fields: `values`, `hidden`, `data`, `value`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"completed"` |

### StepsWidget
- Example ID: `steps1`
- Total fields: **29**
- Key configurable fields: `values`, `hidden`, `data`, `value`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"{{ self.values[0] }}"` |

### StripeCardFormWidget
- Example ID: `stripeCardForm1`
- Total fields: **4**

### SwitchGroup
- Example ID: `switchGroup1`
- Total fields: **47**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"{{ [self.values[0]] }}"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### SwitchWidget2
- Example ID: `switch1`
- Total fields: **20**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `false` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### TableWidget2
- Example ID: `table1`
- Total fields: **134**
- Key configurable fields: `selectedRowKey`, `_columnIds`, `hidden`, `columnOrdering`, `data`, `events`

| Field | Default |
|-------|---------|
| `selectedRowKey` | `null` |
| `_columnIds` | `[10 items]` |
| `hidden` | `false` |
| `columnOrdering` | `[0 items]` |
| `data` | `"{{ tableData.value }}"` |
| `events` | `[5 items]` |

### TableauWidget
- Example ID: `tableau1`
- Total fields: **4**

### TabsWidget2
- Example ID: `tabs1`
- Total fields: **34**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `[0 items]` |
| `value` | `"{{ self.values[0] }}"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### TagsWidget2
- Example ID: `tags1`
- Total fields: **29**
- Key configurable fields: `values`, `hidden`, `data`, `value`, `events`

| Field | Default |
|-------|---------|
| `values` | `[0 items]` |
| `hidden` | `false` |
| `data` | `"["Foo", "Bar", "Baz"]"` |
| `value` | `[0 items]` |
| `events` | `{...0 keys}` |

### TextAnnotationWidget
- Example ID: `annotatedText1`
- Total fields: **4**
- Key configurable fields: `text`

| Field | Default |
|-------|---------|
| `text` | `"I live in San Francisco and my name i..."` |

### TextAreaWidget
- Example ID: `textArea1`
- Total fields: **38**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `""` |
| `placeholder` | `"Enter value"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### TextEditorWidget
- Example ID: `richTextEditor1`
- Total fields: **4**
- Key configurable fields: `value`

| Field | Default |
|-------|---------|
| `value` | `"text"` |

### TextInputWidget2
- Example ID: `textInput1`
- Total fields: **41**
- Key configurable fields: `hidden`, `value`, `placeholder`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `""` |
| `placeholder` | `"Enter value"` |
| `label` | `"Label"` |
| `events` | `[1 items]` |
| `disabled` | `false` |

### TextWidget2
- Example ID: `text1`
- Total fields: **12**
- Key configurable fields: `hidden`, `value`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `"👋 **Hello {{ current_user.firstName |..."` |

### TimeWidget
- Example ID: `time1`
- Total fields: **38**
- Key configurable fields: `hidden`, `value`, `label`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `value` | `"{{ new Date() }}"` |
| `label` | `"Label"` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### TimelineWidget
- Example ID: `eventList1`
- Total fields: **9**

### TimelineWidget2
- Example ID: `timeline1`
- Total fields: **35**
- Key configurable fields: `hidden`, `data`, `events`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `data` | `"[{"id":1,"title":"Website Redesign","..."` |
| `events` | `{...0 keys}` |

### TimerWidget
- Example ID: `timer1`
- Total fields: **6**

### ToggleButtonWidget
- Example ID: `toggleButton1`
- Total fields: **17**
- Key configurable fields: `hidden`, `text`, `value`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `text` | `"{{ self.value ? 'Hide' : 'Show' }}"` |
| `value` | `false` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### ToggleLinkWidget
- Example ID: `toggleLink1`
- Total fields: **15**
- Key configurable fields: `hidden`, `text`, `value`, `events`, `disabled`

| Field | Default |
|-------|---------|
| `hidden` | `false` |
| `text` | `"{{ self.value ? 'Hide' : 'Show' }}"` |
| `value` | `false` |
| `events` | `{...0 keys}` |
| `disabled` | `false` |

### VideoWidget
- Example ID: `video1`
- Total fields: **14**
- Key configurable fields: `src`, `hidden`, `events`

| Field | Default |
|-------|---------|
| `src` | `"https://www.youtube.com/watch?v=dQw4w..."` |
| `hidden` | `false` |
| `events` | `{...0 keys}` |

### WizardWidget
- Example ID: `wizard1`
- Total fields: **11**
- Key configurable fields: `hidden`

| Field | Default |
|-------|---------|
| `hidden` | `false` |

---
## Query Types

### JavascriptQuery
- Example ID: `exampleGlobalJsQuery`
- Total fields: **68**

| Field | Default |
|-------|---------|
| `runWhenModelUpdates` | `false` |
| `showFailureToaster` | `true` |
| `query` | `"// Convert Retool's object-of-arrays ..."` |
| `data` | `null` |
| `importedQueryInputs` | `{...0 keys}` |
| `showSuccessToaster` | `false` |
| `resourceTypeOverride` | `null` |
| `enableTransformer` | `false` |
| `runWhenPageLoads` | `false` |
| `transformer` | `"return data"` |
| `events` | `[3 items]` |
| `queryTimeout` | `"10000"` |
| `notificationDuration` | `4.5` |

### RESTQuery
- Example ID: `ExampleGlobalRestQuery`
- Total fields: **82**

| Field | Default |
|-------|---------|
| `runWhenModelUpdates` | `false` |
| `showFailureToaster` | `true` |
| `query` | `"/fleet/vehicles"` |
| `data` | `null` |
| `importedQueryInputs` | `{...0 keys}` |
| `showSuccessToaster` | `false` |
| `resourceTypeOverride` | `""` |
| `enableTransformer` | `false` |
| `runWhenPageLoads` | `false` |
| `transformer` | `"return data"` |
| `events` | `[2 items]` |
| `queryTimeout` | `"10000"` |
| `notificationDuration` | `4.5` |

### RetoolAIAgentInvokeQuery
- Example ID: `agentChat1_query1`
- Total fields: **74**

| Field | Default |
|-------|---------|
| `runWhenModelUpdates` | `false` |
| `showFailureToaster` | `true` |
| `query` | `""` |
| `data` | `null` |
| `importedQueryInputs` | `{...0 keys}` |
| `showSuccessToaster` | `false` |
| `resourceTypeOverride` | `null` |
| `enableTransformer` | `false` |
| `runWhenPageLoads` | `false` |
| `transformer` | `"return data"` |
| `events` | `[0 items]` |
| `queryTimeout` | `"10000"` |
| `notificationDuration` | `""` |

### RetoolAIQuery
- Example ID: `llmChat1_query1`
- Total fields: **114**

| Field | Default |
|-------|---------|
| `runWhenModelUpdates` | `false` |
| `showFailureToaster` | `true` |
| `query` | `""` |
| `data` | `null` |
| `importedQueryInputs` | `{...0 keys}` |
| `showSuccessToaster` | `true` |
| `resourceTypeOverride` | `null` |
| `enableTransformer` | `false` |
| `runWhenPageLoads` | `false` |
| `transformer` | `"return data"` |
| `events` | `[1 items]` |
| `queryTimeout` | `"120000"` |
| `notificationDuration` | `""` |

### SqlQueryUnified
- Example ID: `exampleGlobalSqlQuery`
- Total fields: **89**

| Field | Default |
|-------|---------|
| `runWhenModelUpdates` | `true` |
| `showFailureToaster` | `true` |
| `query` | `"SELECT 1 as id, 'test' as name, now()..."` |
| `data` | `null` |
| `importedQueryInputs` | `{...0 keys}` |
| `showSuccessToaster` | `false` |
| `resourceTypeOverride` | `null` |
| `enableTransformer` | `true` |
| `runWhenPageLoads` | `false` |
| `transformer` | `"// 'data' here is the raw result of t..."` |
| `events` | `[7 items]` |
| `queryTimeout` | `"10000"` |
| `notificationDuration` | `4.5` |

---
## Frame Types

### $main
- Total fields: **5**
- Fields: `type`, `padding`, `enableFullBleed`, `isHiddenOnDesktop`, `isHiddenOnMobile`

### $main2
- Total fields: **6**
- Fields: `type`, `sticky`, `padding`, `enableFullBleed`, `isHiddenOnDesktop`, `isHiddenOnMobile`

### drawerFrame1
- Total fields: **18**
- Fields: `hideOnEscape`, `overlayInteraction`, `headerPadding`, `showFooterBorder`, `width`, `enableFullBleed`, `isHiddenOnDesktop`, `showBorder`, `hidden`, `showHeader`, `padding`, `showOverlay`, `isHiddenOnMobile`, `showHeaderBorder`, `footerPadding`, `showFooter`, `events`, `loading`

### modalFrame1
- Total fields: **18**
- Fields: `size`, `hideOnEscape`, `overlayInteraction`, `headerPadding`, `showFooterBorder`, `enableFullBleed`, `isHiddenOnDesktop`, `showBorder`, `hidden`, `showHeader`, `padding`, `showOverlay`, `isHiddenOnMobile`, `showHeaderBorder`, `footerPadding`, `showFooter`, `events`, `loading`

### splitPaneFrame1
- Total fields: **17**
- Fields: `headerPadding`, `showFooterBorder`, `_resizeHandleEnabled`, `width`, `enableFullBleed`, `isHiddenOnDesktop`, `position`, `showBorder`, `hidden`, `showHeader`, `padding`, `isHiddenOnMobile`, `showHeaderBorder`, `footerPadding`, `showFooter`, `events`, `loading`

---
## Event Patterns

These are real event handler structures extracted from the components example.
Each event uses `tom()` (ordered map) encoding — NEVER `tmap()`.

**45 unique event patterns:**

| Event | Method | Type | Plugin ID |
|-------|--------|------|-----------|
| `{'id': '538e9ae4', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce', 'event': 'clickToolbar', 'method': 'exportData', 'pluginId': 'table2', 'targetId': '3c'}` | `?` | `?` | `` |
| `{'id': '5515b44c', 'params': {'wrap': False}, 'event': 'click', 'method': 'showNextVisibleView', 'pluginId': 'steppedContainer1', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce'}` | `?` | `?` | `` |
| `{'id': '65bf86c3', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce', 'event': 'clickToolbar', 'method': 'exportData', 'pluginId': 'table1', 'targetId': '3c'}` | `?` | `?` | `` |
| `{'id': '7cee3c4f', 'params': {'wrap': False}, 'event': 'click', 'method': 'showPreviousVisibleView', 'pluginId': 'steppedContainer1', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce'}` | `?` | `?` | `` |
| `{'id': '86423d3a', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce', 'event': 'clickToolbar', 'method': 'refresh', 'pluginId': 'table1', 'targetId': '4d'}` | `?` | `?` | `` |
| `{'id': '9e0cfc7a', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce', 'event': 'clickToolbar', 'method': 'refresh', 'pluginId': 'table2', 'targetId': '4d'}` | `?` | `?` | `` |
| `{'id': 'a84aaebf', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce', 'event': 'clickToolbar', 'method': 'refresh', 'pluginId': 'table3', 'targetId': '4d'}` | `?` | `?` | `` |
| `{'id': 'aade5d88', 'event': 'click', 'type': 'widget', 'method': 'setHidden', 'pluginId': 'modalFrame1', 'params': {'hidden': True}, 'waitType': 'debounce', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'id': 'ad09f2a9', 'params': {'showBody': '{{ self.value }}'}, 'event': 'change', 'method': 'setShowBody', 'pluginId': 'collapsibleContainer1', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce'}` | `?` | `?` | `` |
| `{'id': 'd51b8c8c', 'event': 'click', 'type': 'widget', 'method': 'setHidden', 'pluginId': 'drawerFrame1', 'params': {'hidden': True}, 'waitType': 'debounce', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'id': 'd786d740', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce', 'event': 'clickToolbar', 'method': 'exportData', 'pluginId': 'table3', 'targetId': '3c'}` | `?` | `?` | `` |
| `{'id': 'mockEventHandlerId1', 'event': 'click', 'method': 'confetti', 'pluginId': '', 'type': 'util', 'waitType': 'debounce'}` | `?` | `?` | `` |
| `{'id': 'mockEventHandlerId1', 'event': 'click', 'type': 'util', 'method': 'openPage', 'pluginId': '', 'waitType': 'debounce', 'waitMs': '0', 'params': {'pageName': '{{ item.id }}'}}` | `?` | `?` | `` |
| `{'id': 'mockEventHandlerId1', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce', 'event': 'clickHeader', 'method': 'clearHistory', 'pluginId': 'llmChat1', 'targetId': '3c'}` | `?` | `?` | `` |
| `{'id': 'mockEventHandlerId1', 'type': 'widget', 'waitMs': '0', 'waitType': 'debounce', 'event': 'clickHeader', 'method': 'exportData', 'pluginId': 'llmChat1', 'targetId': '2b'}` | `?` | `?` | `` |
| `{'method': 'copyToClipboard', 'params': {'value': '{{ currentMessage.value }}'}, 'targetId': '1a', 'pluginId': 'commentThread1', 'waitType': 'debounce', 'event': 'clickAction', 'type': 'util', 'id': 'mockEventHandlerId1', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'copyToClipboard', 'params': {'value': '{{ currentMessage.value }}'}, 'targetId': '1a', 'pluginId': 'llmChat1', 'waitType': 'debounce', 'event': 'clickAction', 'type': 'util', 'id': 'mockEventHandlerId1', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'openPage', 'params': {'options': {'passDataWith': 'urlParams'}, 'pageName': 'page2'}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'click', 'type': 'util', 'id': 'ca538323', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'openUrl', 'params': {'url': '~`https://docs.retool.com`'}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'click', 'type': 'util', 'id': '4f6904b2', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'run', 'params': {'src': 'addUserToTable.trigger()'}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'submit', 'type': 'script', 'id': '1478ef69', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'run', 'params': {'src': 'exampleGlobalNone.setValue(exampleGlobalSqlQuery.data)'}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'success', 'type': 'script', 'id': 'e25997f1', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'run', 'params': {'src': 'exampleGlobalNone.setValue(llmChat1_query1.data)'}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'success', 'type': 'script', 'id': '95080466', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'run', 'params': {'src': 'exampleGlobalNone.setValue(numberInput1.value)'}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'change', 'type': 'script', 'id': 'c1f7fa4f', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'run', 'params': {'src': 'exampleGlobalNone.setValue(textInput1.value)'}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'change', 'type': 'script', 'id': 'b6969a10', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'run', 'params': {'src': 'form1.clear()'}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'submit', 'type': 'script', 'id': '02182f8f', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'run', 'params': {'src': 'form3.clear()'}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'submit', 'type': 'script', 'id': 'c5fbf791', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'setValue', 'params': {'value': 'test value'}, 'targetId': None, 'pluginId': 'exampleGlobalNone', 'waitType': 'debounce', 'event': 'success', 'type': 'state', 'id': '94b28abd', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'setValue', 'params': {'value': '{{ exampleGlobalJsQuery.data }}'}, 'targetId': None, 'pluginId': 'exampleGlobalNone', 'waitType': 'debounce', 'event': 'success', 'type': 'state', 'id': '7540d8d2', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'setValue', 'params': {}, 'targetId': None, 'pluginId': 'exampleGlobalNone', 'waitType': 'debounce', 'event': 'success', 'type': 'state', 'id': 'e952e9db', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'show', 'params': {}, 'targetId': 'c8d03', 'pluginId': 'modalFrame1', 'waitType': 'debounce', 'event': 'clickAction', 'type': 'widget', 'id': 'b5299f9d', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'showNotification', 'params': {'options': {'notificationType': 'error', 'title': 'error '}}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'failure', 'type': 'util', 'id': 'fae26c24', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'showNotification', 'params': {'options': {'notificationType': 'info', 'title': 'API request failed', 'description': '{{ ExampleGlobalRestQuery.error }}'}}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'failure', 'type': 'util', 'id': '30505e11', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'showNotification', 'params': {'options': {'notificationType': 'info', 'title': 'SQL query failed', 'description': '{{ exampleGlobalSqlQuery.error }}', 'duration': '6'}}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'failure', 'type': 'util', 'id': '044e209d', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'showNotification', 'params': {'options': {'notificationType': 'info', 'title': 'sql query complete', 'description': '~`Fetched {{ exampleGlobalSqlQuery.data.length }} rows`'}}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'success', 'type': 'util', 'id': '3acb3def', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'showNotification', 'params': {'options': {'notificationType': 'info', 'title': '~`JavaScript error`', 'description': '{{ exampleGlobalJsQuery.error }}', 'duration': '6'}}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'failure', 'type': 'util', 'id': 'cdaedf81', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'showNotification', 'params': {'options': {'notificationType': 'success', 'title': 'Processing complete'}}, 'targetId': None, 'pluginId': '', 'waitType': 'debounce', 'event': 'success', 'type': 'util', 'id': 'd92fc6ec', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'trigger', 'params': {}, 'targetId': 'fd9bd', 'pluginId': 'exampleGlobalSqlQuery', 'waitType': 'debounce', 'event': 'clickAction', 'type': 'datasource', 'id': '8bbc75fd', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'trigger', 'params': {}, 'targetId': None, 'pluginId': 'addUserToTable', 'waitType': 'debounce', 'event': 'selectRow', 'type': 'datasource', 'id': '2a607ace', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'trigger', 'params': {}, 'targetId': None, 'pluginId': 'exampleChainQuery', 'waitType': 'debounce', 'event': 'click', 'type': 'datasource', 'id': 'de8b5e0d', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'trigger', 'params': {}, 'targetId': None, 'pluginId': 'exampleGlobalJsQuery', 'waitType': 'debounce', 'event': 'click', 'type': 'datasource', 'id': '35c5c323', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'trigger', 'params': {}, 'targetId': None, 'pluginId': 'exampleGlobalJsQuery', 'waitType': 'debounce', 'event': 'success', 'type': 'datasource', 'id': '57d7e028', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'trigger', 'params': {}, 'targetId': None, 'pluginId': 'exampleGlobalJsQuery', 'waitType': 'debounce', 'event': 'success', 'type': 'datasource', 'id': 'c54d5004', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'trigger', 'params': {}, 'targetId': None, 'pluginId': 'exampleGlobalSqlQuery', 'waitType': 'debounce', 'event': 'change', 'type': 'datasource', 'id': '0f934a48', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'trigger', 'params': {}, 'targetId': None, 'pluginId': 'exampleGlobalSqlQuery', 'waitType': 'debounce', 'event': 'change', 'type': 'datasource', 'id': '2e1b919d', 'waitMs': '0'}` | `?` | `?` | `` |
| `{'method': 'trigger', 'params': {}, 'targetId': None, 'pluginId': 'exampleGlobalSqlQuery', 'waitType': 'debounce', 'event': 'submit', 'type': 'datasource', 'id': 'e73cd108', 'waitMs': '0'}` | `?` | `?` | `` |

---
## State Variable Templates

- **exampleGlobalNone**: `{'value': '""', 'margin': '4px 8px'}`
- **examplePageNone**: `{'value': '""'}`
- **tableData**: `{'value': '[{"id":0,"firstName":"Chic","lastName":"Footitt","email":"chic.footitt@yahoo.com","website":"https://chic.footitt.com","text":"Nulla sit amet nibh at augue facilisis viverra quis id dui. Nullam mattis ultricies metus. Donec eros lorem, egestas vitae aliquam quis, rutrum a mauris","role":"Viewer","teams":["Workplace","Infrastructure"],"enabled":true,"createdAt":"2023-01-16T23:40:20.385Z"},{"id":1,"firstName":"Kenton","lastName":"Worling","email":"kentonworling@yahoo.com","website":"https://kenton.worling.com","text":"Duis viverra elementum ante, placerat sollicitudin ipsum laoreet nec.. Suspendisse et lacus augue. Nullam mattis ultricies metus. Etiam bibendum auctor aliquet. Proin scelerisque molestie lacinia. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus sit amet metus velit. Phasellus bibendum luctus dignissim. Donec eros lorem, egestas vitae aliquam quis, rutrum a mauris","role":"Viewer","teams":["Workplace"],"enabled":false,"createdAt":"2021-12-24T23:40:20.385Z"}]'}`
- **exampleNumberState**: `{'value': '0'}`
- **exampleArrayState**: `{'value': '[]'}`
- **exampleObjectState**: `{'value': '{}'}`
- **examplePage2State**: `{'value': '"page2 default"'}`
