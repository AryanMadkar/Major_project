# Model Evaluation Report (All Single-Property Messages)

- Generated: 2026-05-28T19:36:58
- Endpoint: http://127.0.0.1:8000/extract
- Total messages: 16
- Overall supported fields: 93/127
- Overall accuracy: 73.23%

## 1. single_property_Dataset/rent/01.md

- Sample accuracy: 88.24% (15/17)

### Original message

```text
🏢 1BHK FLAT ON RENT 🏢
👉🏻 Available Semi Furnished R Flat 1BHK On Rent at Ganesh Chowk, Charkop, kandivali west,
👉🏻 North Facing, with Gas pipe Line Connection
👉🏻 walking Distance of Kandivali Metro Station
💰 Rent 33000/-   &
Deposit of Rs 1,50,000/-
📞 Please Contact :
BHOOMI ASSOCAITES
9867722289
7977756496
```

### Model response

```json
{
  "amenities": [
    "air conditioning"
  ],
  "attributes": {
    "facing": "north",
    "furnishing": "semi_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": [
        "air conditioning"
      ]
    },
    "attributes.facing": {
      "confidence": 85,
      "end": 117,
      "extractor": "facing_regex",
      "repair_history": [],
      "source": "keyword",
      "source_span": "north facing",
      "start": 105,
      "value": "north"
    },
    "attributes.furnishing": {
      "confidence": 80,
      "end": 42,
      "extractor": "furnishing_keyword_scorer",
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": "semi furnished",
      "start": 28,
      "value": "semi_furnished"
    },
    "location.locations": {
      "confidence": 80,
      "end": 87,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "charkop",
      "start": 80,
      "value": [
        "charkop",
        "kandivali",
        "kandivali west",
        "metro station"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "end": 87,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "charkop",
      "start": 80,
      "value": "charkop"
    },
    "location.railway_line": {
      "confidence": 85,
      "end": 98,
      "extractor": "location_railway_dict",
      "repair_history": [],
      "source": "dictionary",
      "source_span": "kandivali",
      "start": 89,
      "value": "western"
    },
    "metadata.contact_numbers": {
      "confidence": 95,
      "end": 281,
      "extractor": "phone_regex_or_llm",
      "repair_history": [],
      "source": "regex+llm",
      "source_span": "7977756496, 9867722289",
      "start": 260,
      "value": [
        "7977756496",
        "9867722289"
      ]
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 87,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "1bhk flat on rent available semi furnished r flat 1bhk on rent at ganesh chowk, charkop",
      "start": 0,
      "value": "1BHK Apartment For Rent in Charkop"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 90,
      "end": 204,
      "extractor": "price_deposit_keyword_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 33000 ",
      "start": 197,
      "value": 33000
    },
    "pricing.price": {
      "confidence": 85,
      "end": 204,
      "extractor": "price_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 33000 ",
      "start": 197,
      "value": 33000
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 90,
      "end": 204,
      "extractor": "price_rent_keyword_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 33000 ",
      "start": 197,
      "value": 33000
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 9,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 5,
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 9,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 5,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 4,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "1bhk",
      "start": 0,
      "value": 1
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 17,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "rent",
      "start": 13,
      "value": "rent"
    }
  },
  "location": {
    "locations": [
      "charkop",
      "kandivali",
      "kandivali west",
      "metro station"
    ],
    "primary_location": "charkop",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [
      "7977756496",
      "9867722289"
    ],
    "contact_people": [],
    "message_title": "1BHK Apartment For Rent in Charkop",
    "metadata_summary": {
      "has_contact": true,
      "total_contacts": 0,
      "total_numbers": 2
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": 33000,
    "price": 33000,
    "price_max": null,
    "price_min": null,
    "rent_price": 33000
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "rent"
  }
}
```

## 2. single_property_Dataset/rent/02.md

- Sample accuracy: 50.00% (3/6)

### Original message

```text
1 bhk fully furnished in blue empire@36000 negotiable

For more details Contact
Rajan sarawagi
9821452541
```

### Model response

```json
{
  "amenities": [
    "air conditioning"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": [
        "air conditioning"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "end": 21,
      "extractor": "furnishing_keyword_scorer",
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": "fully furnished",
      "start": 6,
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 95,
      "end": 104,
      "extractor": "phone_regex_or_llm",
      "repair_history": [],
      "source": "regex+llm",
      "source_span": "9821452541",
      "start": 94,
      "value": [
        "9821452541"
      ]
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 5,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "1 bhk",
      "start": 0,
      "value": "1BHK Apartment"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 5,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "1 bhk",
      "start": 0,
      "value": 1
    },
    "summary.request_type": {
      "confidence": 90,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": null,
      "start": null,
      "value": "unknown"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [
      "9821452541"
    ],
    "contact_people": [],
    "message_title": "1BHK Apartment",
    "metadata_summary": {
      "has_contact": true,
      "total_contacts": 0,
      "total_numbers": 1
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "unknown"
  }
}
```

## 3. single_property_Dataset/rent/03.md

- Sample accuracy: 60.00% (3/5)

### Original message

```text
🏠 2 bhk for rent in veena smart homes@49000

Semi furnished flat
Family preferred
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "end": 61,
      "extractor": "furnishing_keyword_scorer",
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": "furnished flat",
      "start": 47,
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 61,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "2 bhk for rent in veena smart homes 49000 semi furnished flat",
      "start": 0,
      "value": "2BHK Apartment For Rent"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 61,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 57,
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 61,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 57,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 5,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "2 bhk",
      "start": 0,
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 14,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "rent",
      "start": 10,
      "value": "rent"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment For Rent",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "rent"
  }
}
```

## 4. single_property_Dataset/rent/04.md

- Sample accuracy: 85.71% (6/7)

### Original message

```text
3 bhk on rent in hiranandani heritage, sv road, poisar, @90000

Fully furnished
Higher floor
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "end": 77,
      "extractor": "furnishing_keyword_scorer",
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": "fully furnished",
      "start": 62,
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 80,
      "end": 46,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "sv road",
      "start": 39,
      "value": [
        "sv road",
        "poisar"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "end": 46,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "sv road",
      "start": 39,
      "value": "sv road"
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 46,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "3 bhk on rent in hiranandani heritage, sv road",
      "start": 0,
      "value": "3BHK Apartment For Rent in Sv Road"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 5,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "3 bhk",
      "start": 0,
      "value": 3
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 13,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "rent",
      "start": 9,
      "value": "rent"
    }
  },
  "location": {
    "locations": [
      "sv road",
      "poisar"
    ],
    "primary_location": "sv road",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "3BHK Apartment For Rent in Sv Road",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "rent"
  }
}
```

## 5. single_property_Dataset/rent/049.md

- Sample accuracy: 55.56% (5/9)

### Original message

```text
2 Bhk Rental Flat In Uk Iridium
Semi Furnished Flat With Modular Kitchen
Rent 45k Deposit 1.25 lakh
```

### Model response

```json
{
  "amenities": [
    "modular kitchen"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "semi_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": 72,
      "extractor": "amenities_automaton_or_llm",
      "repair_history": [],
      "source": "regex+llm",
      "source_span": "modular kitchen",
      "start": 57,
      "value": [
        "modular kitchen"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "end": 46,
      "extractor": "furnishing_keyword_scorer",
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": "semi furnished",
      "start": 32,
      "value": "semi_furnished"
    },
    "location.locations": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 17,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "2 bhk rental flat",
      "start": 0,
      "value": "2BHK Apartment For Rent"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 90,
      "end": 81,
      "extractor": "price_deposit_keyword_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 45k",
      "start": 77,
      "value": 45000
    },
    "pricing.price": {
      "confidence": 85,
      "end": 96,
      "extractor": "price_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 1.25 l",
      "start": 89,
      "value": 125000
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 90,
      "end": 81,
      "extractor": "price_rent_keyword_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 45k",
      "start": 77,
      "value": 45000
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 17,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 13,
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 17,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 13,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 5,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "2 bhk",
      "start": 0,
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 77,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "rent",
      "start": 73,
      "value": "rent"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment For Rent",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": 45000,
    "price": 125000,
    "price_max": null,
    "price_min": null,
    "rent_price": 45000
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "rent"
  }
}
```

## 6. single_property_Dataset/requirements/01.md

- Sample accuracy: 80.00% (8/10)

### Original message

```text
OM SAI RAM
🏠REQUIRED 1 BHK FLAT FOR OUT RATE BUDGET 1 CR TO 1.10 CR
LOCATION ANY CHARKOP SECTOR
KANDIVALI WEST

CALL
9820067788
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.locations": {
      "confidence": 80,
      "end": 87,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "charkop",
      "start": 80,
      "value": [
        "charkop",
        "kandivali",
        "kandivali west"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "end": 87,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "charkop",
      "start": 80,
      "value": "charkop"
    },
    "location.railway_line": {
      "confidence": 85,
      "end": 104,
      "extractor": "location_railway_dict",
      "repair_history": [],
      "source": "dictionary",
      "source_span": "kandivali",
      "start": 95,
      "value": "western"
    },
    "metadata.contact_numbers": {
      "confidence": 95,
      "end": 125,
      "extractor": "phone_regex_or_llm",
      "repair_history": [],
      "source": "regex+llm",
      "source_span": "9820067788",
      "start": 115,
      "value": [
        "9820067788"
      ]
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 87,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "1 bhk flat for out rate budget 1 cr to 1.10 cr location any charkop",
      "start": 20,
      "value": "1BHK Apartment in Charkop"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "end": 66,
      "extractor": "price_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 1.10 cr",
      "start": 58,
      "value": 11000000
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 30,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 26,
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 30,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 26,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 25,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "1 bhk",
      "start": 20,
      "value": 1
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 19,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "required",
      "start": 11,
      "value": "requirement"
    }
  },
  "location": {
    "locations": [
      "charkop",
      "kandivali",
      "kandivali west"
    ],
    "primary_location": "charkop",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [
      "9820067788"
    ],
    "contact_people": [],
    "message_title": "1BHK Apartment in Charkop",
    "metadata_summary": {
      "has_contact": true,
      "total_contacts": 0,
      "total_numbers": 1
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 11000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "requirement"
  }
}
```

## 7. single_property_Dataset/requirements/02.md

- Sample accuracy: 71.43% (5/7)

### Original message

```text
Need 2 bhk flat on rent
Budget 45000
Near metro preferred
Family client

Contact urgently
```

### Model response

```json
{
  "amenities": [
    "air conditioning"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": [
        "air conditioning"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.locations": {
      "confidence": 80,
      "end": 71,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "near metro preferred family client",
      "start": 37,
      "value": [
        "near metro preferred family client"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "end": 71,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "near metro preferred family client",
      "start": 37,
      "value": "near metro preferred family client"
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 71,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "2 bhk flat on rent budget 45000 near metro preferred family client",
      "start": 5,
      "value": "2BHK Apartment in Near Metro Preferred Family Client"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 15,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 11,
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 15,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 11,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 10,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "2 bhk",
      "start": 5,
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 4,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "need",
      "start": 0,
      "value": "requirement"
    }
  },
  "location": {
    "locations": [
      "near metro preferred family client"
    ],
    "primary_location": "near metro preferred family client",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment in Near Metro Preferred Family Client",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "requirement"
  }
}
```

## 8. single_property_Dataset/requirements/03.md

- Sample accuracy: 60.00% (6/10)

### Original message

```text
Urgent Requirement

3 bhk furnished flat required in Borivali West
Budget 2.5 cr
Immediate closing

Broker pls contact
```

### Model response

```json
{
  "amenities": [
    "air conditioning"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": [
        "air conditioning"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "end": 39,
      "extractor": "furnishing_keyword_scorer",
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": "furnished flat",
      "start": 25,
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 80,
      "end": 60,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "borivali",
      "start": 52,
      "value": [
        "borivali",
        "borivali west"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "end": 60,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "borivali",
      "start": 52,
      "value": "borivali"
    },
    "location.railway_line": {
      "confidence": 85,
      "end": 60,
      "extractor": "location_railway_dict",
      "repair_history": [],
      "source": "dictionary",
      "source_span": "borivali",
      "start": 52,
      "value": "western"
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 60,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "3 bhk furnished flat required in borivali",
      "start": 19,
      "value": "3BHK Apartment in Borivali"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "end": 79,
      "extractor": "price_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 2.5 cr",
      "start": 72,
      "value": 25000000
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 39,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 35,
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 39,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 35,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 24,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "3 bhk",
      "start": 19,
      "value": 3
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 48,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "required",
      "start": 40,
      "value": "requirement"
    }
  },
  "location": {
    "locations": [
      "borivali",
      "borivali west"
    ],
    "primary_location": "borivali",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "3BHK Apartment in Borivali",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 25000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "requirement"
  }
}
```

## 9. single_property_Dataset/requirements/04.md

- Sample accuracy: 60.00% (3/5)

### Original message

```text
Requirement for investor client

Need 2 bhk flat for outright purchase
Budget upto 2 cr
Ready possession only
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 47,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "2 bhk flat",
      "start": 37,
      "value": "2BHK Apartment"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "end": 86,
      "extractor": "price_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 2 cr",
      "start": 81,
      "value": 20000000
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 47,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 43,
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 47,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 43,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 42,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "2 bhk",
      "start": 37,
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 11,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "requirement",
      "start": 0,
      "value": "requirement"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 20000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "requirement"
  }
}
```

## 10. single_property_Dataset/requirements/049.md

- Sample accuracy: 85.71% (6/7)

### Original message

```text
Need commercial office on rent
300 carpet minimum
Near link road preferred

Immediate possession required
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.locations": {
      "confidence": 80,
      "end": 84,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "near link road preferred immediate",
      "start": 50,
      "value": [
        "near link road preferred immediate",
        "link road"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "end": 84,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "near link road preferred immediate",
      "start": 50,
      "value": "near link road preferred immediate"
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 84,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "office on rent 300 carpet minimum near link road preferred immediate",
      "start": 16,
      "value": "Office in Near Link Road Preferred Immediate"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 22,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "office",
      "start": 16,
      "value": [
        "office",
        "commercial_space"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 22,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "office",
      "start": 16,
      "value": "office"
    },
    "summary.bhk": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 104,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "required",
      "start": 96,
      "value": "requirement"
    }
  },
  "location": {
    "locations": [
      "near link road preferred immediate",
      "link road"
    ],
    "primary_location": "near link road preferred immediate",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Office in Near Link Road Preferred Immediate",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "office",
      "commercial_space"
    ],
    "property_subtype": "office"
  },
  "summary": {
    "bhk": null,
    "request_type": "requirement"
  }
}
```

## 11. single_property_Dataset/requirements/06.md

- Sample accuracy: 100.00% (4/4)

### Original message

```text
Client Requirement

Need 4 bhk bungalow in Lonavala
Budget flexible
Ready to move preferred
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 38,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "4 bhk bungalow",
      "start": 24,
      "value": "4BHK Bungalow"
    },
    "parking.parking_count": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex",
      "source_span": null,
      "start": null,
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 38,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bungalow",
      "start": 30,
      "value": [
        "bungalow"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 38,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bungalow",
      "start": 30,
      "value": "bungalow"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 29,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "4 bhk",
      "start": 24,
      "value": 4
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 18,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "requirement",
      "start": 7,
      "value": "requirement"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "4BHK Bungalow",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "bungalow"
    ],
    "property_subtype": "bungalow"
  },
  "summary": {
    "bhk": 4,
    "request_type": "requirement"
  }
}
```

## 12. single_property_Dataset/sale/01.md

- Sample accuracy: 71.43% (5/7)

### Original message

```text
1 BHK
Kanakya park
With car parking
Asking 1.05 Cr
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": 35,
      "extractor": "amenities_automaton_or_llm",
      "repair_history": [],
      "source": "regex+llm",
      "source_span": "parking",
      "start": 28,
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 5,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "1 bhk",
      "start": 0,
      "value": "1BHK Apartment For Sale"
    },
    "parking.parking_count": {
      "confidence": 80,
      "end": 35,
      "extractor": "parking_generic_fallback",
      "repair_history": [],
      "source": "regex",
      "source_span": "parking",
      "start": 28,
      "value": 1
    },
    "parking.parking_type": {
      "confidence": 80,
      "end": 35,
      "extractor": "parking_type_regex",
      "repair_history": [],
      "source": "keyword",
      "source_span": "car parking",
      "start": 24,
      "value": "car"
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "end": 50,
      "extractor": "price_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 1.05 cr",
      "start": 42,
      "value": 10500000
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 5,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "1 bhk",
      "start": 0,
      "value": 1
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 42,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "asking",
      "start": 36,
      "value": "sale"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "1BHK Apartment For Sale",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 10500000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "sale"
  }
}
```

## 13. single_property_Dataset/sale/02.md

- Sample accuracy: 55.56% (5/9)

### Original message

```text
2 BHK
Radha residency
With car parking
Furnished flat
Asking 2.85 CR
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": 38,
      "extractor": "amenities_automaton_or_llm",
      "repair_history": [],
      "source": "regex+llm",
      "source_span": "parking",
      "start": 31,
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "end": 53,
      "extractor": "furnishing_keyword_scorer",
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": "furnished flat",
      "start": 39,
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 53,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "2 bhk radha residency with car parking furnished flat",
      "start": 0,
      "value": "2BHK Apartment For Sale"
    },
    "parking.parking_count": {
      "confidence": 80,
      "end": 38,
      "extractor": "parking_generic_fallback",
      "repair_history": [],
      "source": "regex",
      "source_span": "parking",
      "start": 31,
      "value": 1
    },
    "parking.parking_type": {
      "confidence": 80,
      "end": 38,
      "extractor": "parking_type_regex",
      "repair_history": [],
      "source": "keyword",
      "source_span": "car parking",
      "start": 27,
      "value": "car"
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "end": 68,
      "extractor": "price_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 2.85 cr",
      "start": 60,
      "value": 28500000
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "end": 53,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 49,
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 53,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "flat",
      "start": 49,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 5,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "2 bhk",
      "start": 0,
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 60,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "asking",
      "start": 54,
      "value": "sale"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment For Sale",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 28500000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "sale"
  }
}
```

## 14. single_property_Dataset/sale/03.md

- Sample accuracy: 71.43% (5/7)

### Original message

```text
3 BHK
Oberoi sky City
Middle floor
2 car parking
Asking 4.7Cr
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": 48,
      "extractor": "amenities_automaton_or_llm",
      "repair_history": [],
      "source": "regex+llm",
      "source_span": "parking",
      "start": 41,
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 5,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "3 bhk",
      "start": 0,
      "value": "3BHK Apartment For Sale"
    },
    "parking.parking_count": {
      "confidence": 80,
      "end": 48,
      "extractor": "parking_count_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "2 car parking",
      "start": 35,
      "value": 2
    },
    "parking.parking_type": {
      "confidence": 80,
      "end": 48,
      "extractor": "parking_type_regex",
      "repair_history": [],
      "source": "keyword",
      "source_span": "car parking",
      "start": 37,
      "value": "car"
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "end": 61,
      "extractor": "price_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 4.7cr",
      "start": 55,
      "value": 47000000
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 5,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "3 bhk",
      "start": 0,
      "value": 3
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 55,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "asking",
      "start": 49,
      "value": "sale"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "3BHK Apartment For Sale",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 2,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 47000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "sale"
  }
}
```

## 15. single_property_Dataset/sale/04.md

- Sample accuracy: 80.00% (4/5)

### Original message

```text
🔹 3 BHK | 1036 Sqft | 22nd Floor
💰 ₹3.78 Cr
✅ OC June 2025 | Immediate Possession | 1 Parking
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": 79,
      "extractor": "amenities_automaton_or_llm",
      "repair_history": [],
      "source": "regex+llm",
      "source_span": "parking",
      "start": 72,
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": null,
      "start": null,
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "dictionary",
      "source_span": null,
      "start": null,
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 5,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "3 bhk",
      "start": 0,
      "value": "3BHK Apartment For Sale"
    },
    "parking.parking_count": {
      "confidence": 80,
      "end": 79,
      "extractor": "parking_count_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "1 parking",
      "start": 70,
      "value": 1
    },
    "parking.parking_type": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 5,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "3 bhk",
      "start": 0,
      "value": 3
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 69,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "immediate possession",
      "start": 49,
      "value": "sale"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "3BHK Apartment For Sale",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "sale"
  }
}
```

## 16. single_property_Dataset/sale/06.md

- Sample accuracy: 83.33% (10/12)

### Original message

```text
2 BHK
Rizvi Cedar Tower
Malad East
Semi furnished
With car parking
Asking 1.62 Cr
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "semi_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "end": 66,
      "extractor": "amenities_automaton_or_llm",
      "repair_history": [],
      "source": "regex+llm",
      "source_span": "parking",
      "start": 59,
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "keyword",
      "source_span": null,
      "start": null,
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "end": 49,
      "extractor": "furnishing_keyword_scorer",
      "repair_history": [],
      "source": "keyword+scoring",
      "source_span": "semi furnished",
      "start": 35,
      "value": "semi_furnished"
    },
    "location.locations": {
      "confidence": 80,
      "end": 23,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "2 bhk rizvi cedar tower",
      "start": 0,
      "value": [
        "2 bhk rizvi cedar tower",
        "malad",
        "malad east"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "end": 23,
      "extractor": "location_dictionary",
      "repair_history": [],
      "source": "dictionary+patterns",
      "source_span": "2 bhk rizvi cedar tower",
      "start": 0,
      "value": "2 bhk rizvi cedar tower"
    },
    "location.railway_line": {
      "confidence": 85,
      "end": 29,
      "extractor": "location_railway_dict",
      "repair_history": [],
      "source": "dictionary",
      "source_span": "malad",
      "start": 24,
      "value": "western"
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+llm",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "llm+cleanup",
      "source_span": null,
      "start": null,
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "end": 23,
      "extractor": "title_rule_generator",
      "repair_history": [],
      "source": "llm+rules",
      "source_span": "2 bhk rizvi cedar tower",
      "start": 0,
      "value": "2BHK Apartment For Sale in 2 Bhk Rizvi Cedar Tower"
    },
    "parking.parking_count": {
      "confidence": 80,
      "end": 66,
      "extractor": "parking_generic_fallback",
      "repair_history": [],
      "source": "regex",
      "source_span": "parking",
      "start": 59,
      "value": 1
    },
    "parking.parking_type": {
      "confidence": 80,
      "end": 66,
      "extractor": "parking_type_regex",
      "repair_history": [],
      "source": "keyword",
      "source_span": "car parking",
      "start": 55,
      "value": "car"
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "end": 81,
      "extractor": "price_regex",
      "repair_history": [],
      "source": "regex+rules",
      "source_span": " 1.62 cr",
      "start": 73,
      "value": 16200000
    },
    "pricing.price_max": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "end": null,
      "extractor": null,
      "repair_history": [],
      "source": "regex+rules",
      "source_span": null,
      "start": null,
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "end": 5,
      "extractor": "property_subtype_keyword",
      "repair_history": [],
      "source": "keyword+llm",
      "source_span": "bhk",
      "start": 2,
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "end": 5,
      "extractor": "bhk_regex",
      "repair_history": [],
      "source": "regex",
      "source_span": "2 bhk",
      "start": 0,
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "end": 73,
      "extractor": "type_keyword_regex",
      "repair_history": [],
      "source": "keyword+rules",
      "source_span": "asking",
      "start": 67,
      "value": "sale"
    }
  },
  "location": {
    "locations": [
      "2 bhk rizvi cedar tower",
      "malad",
      "malad east"
    ],
    "primary_location": "2 bhk rizvi cedar tower",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment For Sale in 2 Bhk Rizvi Cedar Tower",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 16200000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "sale"
  }
}
```
